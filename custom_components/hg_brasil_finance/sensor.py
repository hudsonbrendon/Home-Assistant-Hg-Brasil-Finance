"""
A platform that provides information about currencies, stocks, and taxes.

For more details on this component, refer to the documentation at
https://github.com/hudsonbrendon/Home-Assistant-Hg-Brasil-Finance
"""
import logging

import async_timeout
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.entity import Entity

CONF_KEY = "key"

BASE_URL = "https://api.hgbrasil.com/finance/?key={}"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_KEY): cv.string,
    }
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup sensor platform."""
    key = config["key"]
    session = async_create_clientsession(hass)
    name = "HG Brasil Finance"
    async_add_entities(
        [
            HGBrasilFinanceCurrencieSensor(key, session),
            HGBrasilFinanceStocksSensor(key, session),
            HGBrasilFinanceTaxesSensor(key, session),
        ],
        True,
    )


class HGBrasilFinanceCurrencieSensor(Entity):
    """Currencie Sensor class"""

    def __init__(self, key, session):
        self._name = "HG Brasil Finance Currencies"
        self._state = self._name
        self.session = session
        self._key = key
        self._dollar = 0
        self._euro = 0
        self._pound_sterling = 0
        self._argentine_peso = 0
        self._canadian_dollar = 0
        self._australian_dollar = 0
        self._japanese_yen = 0
        self._renminbi = 0
        self._bitcoin = 0

    async def async_update(self):
        """Update sensor."""
        _LOGGER.debug("%s - Running update", self._name)
        try:
            url = BASE_URL.format(self._key)
            async with async_timeout.timeout(10, loop=self.hass.loop):
                response = await self.session.get(url)
                info = await response.json()
                coins = info["results"]["currencies"]
            self._dollar = coins["USD"]["buy"]
            self._euro = coins["EUR"]["buy"]
            self._pound_sterling = coins["GBP"]["buy"]
            self._argentine_peso = coins["ARS"]["buy"]
            self._canadian_dollar = coins["CAD"]["buy"]
            self._australian_dollar = coins["AUD"]["buy"]
            self._japanese_yen = coins["JPY"]["buy"]
            self._renminbi = coins["CNY"]["buy"]
            self._bitcoin = coins["BTC"]["buy"]
        except Exception as error:
            _LOGGER.debug("%s - Could not update - %s", self._name, error)

    @property
    def name(self):
        """Name."""
        return self._name

    @property
    def state(self):
        """State."""
        return self._state

    @property
    def dollar(self):
        """Value dollar."""
        return self._dollar

    @property
    def euro(self):
        """Value euro."""
        return self._euro

    @property
    def pound_sterling(self):
        """Value Pound Sterling"""
        return self._pound_sterling

    @property
    def argentine_peso(self):
        """Value Argentine Peso"""
        return self._argentine_peso

    @property
    def canadian_dollar(self):
        """Value Canadian Dollar"""
        return self._canadian_dollar

    @property
    def australian_dollar(self):
        """Value Australian Dollar"""
        return self._australian_dollar

    @property
    def japanese_yen(self):
        """Value Japanese Yen"""
        return self._japanese_yen

    @property
    def renminbi(self):
        """Value Renminbi"""
        return self._renminbi

    @property
    def bitcoin(self):
        """Value Bitcoin"""
        return self._bitcoin

    @property
    def icon(self):
        """Icon."""
        return "mdi:cash"

    @property
    def device_state_attributes(self):
        """Attributes."""
        return {
            "name": self.name,
            "dollar": self.dollar,
            "euro": self.euro,
            "pound sterling": self.pound_sterling,
            "argentine peso": self.argentine_peso,
            "canadian dollar": self.canadian_dollar,
            "australian dollar": self.australian_dollar,
            "japanese yen": self.japanese_yen,
            "renminbi": self.renminbi,
            "bitcoin": self.bitcoin,
        }


class HGBrasilFinanceStocksSensor(Entity):
    """Stocks Sensor class"""

    def __init__(self, key, session):
        self._name = "HG Brasil Finance Stocks"
        self._state = self._name
        self.session = session
        self._key = key
        self._ibovespa = {}
        self._nasdaq = {}
        self._cac = {}
        self._nikkei = {}

    async def async_update(self):
        """Update sensor."""
        _LOGGER.debug("%s - Running update", self._name)
        try:
            url = BASE_URL.format(self._key)
            async with async_timeout.timeout(10, loop=self.hass.loop):
                response = await self.session.get(url)
                info = await response.json()
                stocks = info["results"]["stocks"]
            self._ibovespa = stocks["IBOVESPA"]
            self._nasdaq = stocks["NASDAQ"]
            self._cac = stocks["CAC"]
            self._nikkei = stocks["NIKKEI"]
        except Exception as error:
            _LOGGER.debug("%s - Could not update - %s", self._name, error)

    @property
    def name(self):
        """Name."""
        return self._name

    @property
    def state(self):
        """State."""
        return self._state

    @property
    def ibovespa(self):
        """Stock Ibovespa."""
        return dict(
            points=self._ibovespa.get("points", "not available"),
            variation=self._ibovespa.get("variation", "not available"),
        )

    @property
    def nasdaq(self):
        """Stock NASDAQ."""
        return dict(
            points=self._nasdaq.get("points", "not available"),
            variation=self._nasdaq.get("variation", "not available"),
        )

    @property
    def cac(self):
        """Stock CAC."""
        return dict(
            points=self._cac.get("points", "not available"),
            variation=self._cac.get("variation", "not available"),
        )

    @property
    def nikkei(self):
        """Stock NIKKEI."""
        return dict(
            points=self._nikkei.get("points", "not available"),
            variation=self._nikkei.get("variation", "not available"),
        )

    @property
    def icon(self):
        """Icon."""
        return "mdi:cash-multiple"

    @property
    def device_state_attributes(self):
        """Attributes."""
        return {
            "ibovespa": self.ibovespa,
            "nasdaq": self.nasdaq,
            "cac": self.cac,
            "nikkei": self.nikkei,
        }


class HGBrasilFinanceTaxesSensor(Entity):
    """Taxes Sensor class"""

    def __init__(self, key, session):
        self._name = "HG Brasil Finance Taxes"
        self._state = self._name
        self.session = session
        self._key = key
        self._date = ""
        self._cdi = 0
        self._selic = 0
        self._daily_factor = 0
        self._selic_daily = 0
        self._cdi_daily = 0

    async def async_update(self):
        """Update sensor."""
        _LOGGER.debug("%s - Running update", self._name)
        try:
            url = BASE_URL.format(self._key)
            async with async_timeout.timeout(10, loop=self.hass.loop):
                response = await self.session.get(url)
                info = await response.json()
                taxes = info["results"]["taxes"][0]
            self._date = taxes.get("date", "not available")
            self._cdi = taxes.get("cdi", "not available")
            self._selic = taxes.get("selic", "not available")
            self._daily_factor = taxes.get("daily_factor", "not available")
            self._selic_daily = taxes.get("selic_daily", "not available")
            self._cdi_daily = taxes.get("cdi_daily", "not available")
        except Exception as error:
            _LOGGER.debug("%s - Could not update - %s", self._name, error)

    @property
    def name(self):
        """Name."""
        return self._name

    @property
    def state(self):
        """State."""
        return self._state

    @property
    def date(self):
        """Taxes date."""
        return self._date

    @property
    def cdi(self):
        """Taxe CDI."""
        return self._cdi

    @property
    def selic(self):
        """Taxe Selic."""
        return self._selic

    @property
    def daily_factor(self):
        """Taxe Daily Factor."""
        return self._daily_factor

    @property
    def selic_daily(self):
        """Taxe Selic Daily."""
        return self._selic_daily

    @property
    def cdi_daily(self):
        """Taxe CDI Daily."""
        return self._cdi_daily

    @property
    def icon(self):
        """Icon."""
        return "mdi:cash-100"

    @property
    def device_state_attributes(self):
        """Attributes."""
        return {
            "date": self.date,
            "cdi": self._cdi,
            "selic": self._selic,
            "daily factor": self._daily_factor,
            "selic daily": self._selic_daily,
            "cdi daily": self._cdi_daily,
        }
