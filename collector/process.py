from time import time

from lib.cco import CCOProfile
from lib.sct import AsyncCharge


class CollectorProcess(object):

    def __init__(self, *args, **kwargs):
        self._logger = kwargs['logger']
        self._dispatch_info = kwargs['dispatch_info']
        self._cco = kwargs['cco_profile']
        self._dispatch_content = kwargs.get('dispatch_content', None)

    def cco_charge(self):
        self._cco_charge = CCOProfile(
            brand_id=self._cco['brand_id'],
            partner_id=self._cco['partner_id'],
            product_id=self._cco['product_id'],
            application_id=self._cco['application_id'],
            is_sync=self._cco['is_sync'],
            username=self._cco['username'],
            password=self._cco['password'],
            url=self._cco['url']
        )

        self.msisdn = self._cco['destinations'][0]

        self._logger.info('Charging Brand %s; ANI: %s; Product ID: %s' % (
            self._cco['brand_id'], self.msisdn, self._cco['product_id']
        ))

        start_time = time()
        self._cco_charge.charge(self.msisdn)
        request_lenght = time() - start_time

        self._logger.info('Charge request time: [%.2fs]' % (request_lenght))

    def is_cco_charge_ok(self):
        return self._cco_charge['response'] == 0

    def club_notify(self):
        raise NotImplementedError('Programe aqui')

    def is_async_fallbackeable(self):
        return self._cco['is_sync'] and self._cco['async_fallback']

    def sct_async_charge(self):
        async_charge = AsyncCharge(
            'brand_id': self._cco['brand_id'],
            'partner_id': self._cco['partner_id'],
            'product_id': self._cco['product_id'],
            'application_id': self._cco['application_id'],
            'msisdn': self.msisdn,
            'is_sync': False,
            'username': self._cco['username'],
            'password': self._cco['password'],
            'url': self._cco['url'],
            'service_id': self._cco['service_id']
        )

        async_charge.charge()

    def ignore_charge_result(self):
        return self._cco['ignore_charge_result']

    def is_dispatch_sendeable(self):
        return not self.ignore_charge_result() and self.is_cco_charge_ok()

    def enable_dispatch_send(self):
        raise NotImplementedError('Programe aqui')


