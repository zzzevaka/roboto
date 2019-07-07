from django.db import models
from oanda.api_client import get_oanda_api_client
from roboto.models import Instrument
from strategy.models import Strategy


API = get_oanda_api_client()


class Account(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    alias = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

#
# class Instrument(models.Model):
#     name = models.CharField(max_length=100, db_index=True)
#     type = models.CharField(max_length=100, db_index=True)


class Candle(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True, null=True)

    bid_open = models.FloatField(blank=True, null=True)
    bid_close = models.FloatField(blank=True, null=True)
    bid_low = models.FloatField(blank=True, null=True)
    bid_high = models.FloatField(blank=True, null=True)

    ask_open = models.FloatField(blank=True, null=True)
    ask_close = models.FloatField(blank=True, null=True)
    ask_low = models.FloatField(blank=True, null=True)
    ask_high = models.FloatField(blank=True, null=True)

    mid_open = models.FloatField(blank=True, null=True)
    mid_close = models.FloatField(blank=True, null=True)
    mid_low = models.FloatField(blank=True, null=True)
    mid_high = models.FloatField(blank=True, null=True)


class TradeQuerySet(models.QuerySet):
    def opened(self):
        return self.filter(
            status=Trade.STATUS_OPEN
        )


class Trade(models.Model):
    STATUS_INIT = 0
    STATUS_OPEN = 1
    STATUS_CLOSE = 2
    STATUS_CANCEL = 3
    STATUS_OPEN_ERROR = 4
    STATUS_CLOSE_ERROR = 5

    STATUS_CHOICES = (
        (STATUS_INIT, 'init'),
        (STATUS_OPEN, 'open'),
        (STATUS_CLOSE, 'close'),
        (STATUS_CANCEL, 'cancel'),
        (STATUS_OPEN_ERROR, 'open error'),
        (STATUS_CLOSE_ERROR, 'close error'),
    )

    trade_id = models.SmallIntegerField(null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, on_delete=models.SET_NULL, null=True, related_name='trades')
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_INIT)
    created_at = models.DateTimeField(null=True)
    closed_at = models.DateTimeField(null=True)
    units = models.SmallIntegerField()
    pl = models.FloatField(null=True)

    trade_opened = models.TextField(null=True)
    trade_closed = models.TextField(null=True)

    objects = models.Manager.from_queryset(TradeQuerySet)

    def open(self):
        try:
            create_response = API.order.market(
                accountID=self.account.external_id,
                instrument=self.instrument.name,
                units=self.units,
            )
            if create_response.reason != 'Created':
                raise ValueError('order creating failed cause: {}'.format(create_response.reason))

            if 'orderCancelTransaction' in create_response.body:
                self.status = self.STATUS_CANCEL
                return

            order_create_transaction = create_response.body['orderCreateTransaction']
            self.transactions.create(
                type=Transaction.TYPE_ORDER_CREATE,
                external_id=order_create_transaction.id,
                time=order_create_transaction.time,
                data=order_create_transaction.json(),
            )

            order_fill_transaction = create_response.body['orderFillTransaction']
            self.transactions.create(
                type=Transaction.TYPE_ORDER_FILL,
                external_id=order_fill_transaction.id,
                time=order_fill_transaction.time,
                data=order_fill_transaction.json(),
            )

            self.created_at = order_create_transaction.time
            self.trade_id = order_fill_transaction.tradeOpened.tradeID
            self.trade_opened = order_fill_transaction.tradeOpened.json()
            self.status = self.STATUS_OPEN

        except Exception:
            self.status = self.STATUS_OPEN_ERROR
            raise
        finally:
            self.save()

    def close(self):
        try:
            close_response = API.trade.close(
                accountID=self.account.external_id,
                tradeSpecifier=self.trade_id,
            )

            if not close_response.reason == 'OK':
                raise ValueError('order closing failed cause: {}'.format(close_response.reason))

            order_create_transaction = close_response.body['orderCreateTransaction']
            self.transactions.create(
                type=Transaction.TYPE_ORDER_CREATE,
                external_id=order_create_transaction.id,
                time=order_create_transaction.time,
                data=order_create_transaction.json(),
            )

            order_fill_transaction = close_response.body['orderFillTransaction']
            self.transactions.create(
                type=Transaction.TYPE_ORDER_FILL,
                external_id=order_fill_transaction.id,
                time=order_fill_transaction.time,
                data=order_fill_transaction.json(),
            )

            trade_closed = order_fill_transaction.tradesClosed[0]
            assert trade_closed.tradeID == self.trade_id

            self.closed_at = order_fill_transaction.time
            self.pl = trade_closed.realizedPL
            self.trade_closed = trade_closed.json()
            self.status = self.STATUS_CLOSE
        except Exception:
            self.status = self.STATUS_CLOSE_ERROR
            raise
        finally:
            self.save()


class Transaction(models.Model):
    TYPE_ORDER_CREATE = 0
    TYPE_ORDER_FILL = 1
    TYPE_CHOICES = (
        (TYPE_ORDER_CREATE, 'order create'),
        (TYPE_ORDER_FILL, 'fill'),
    )

    external_id = models.IntegerField()
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='transactions')
    time = models.DateTimeField(null=True)
    type = models.SmallIntegerField(choices=TYPE_CHOICES)
    data = models.TextField()
