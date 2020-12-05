from datetime import datetime
from typing import List, Tuple, Dict
from pathlib import Path
from enum import Enum

from requests_html import HTMLSession
from loguru import logger

from stockmonitor.models.domain.fund import SITCAFormValue, SITCAExpenseTable, create_from_sitca_expense


class SITCAFormMeta(Enum):
    YEAR_ID = 'ctl00_ContentPlaceHolder1_ddlQ_Y'
    YEAR_NAME = 'ctl00$ContentPlaceHolder1$ddlQ_Y'
    MONTH_ID = 'ctl00_ContentPlaceHolder1_ddlQ_M'
    MONTH_NAME = 'ctl00$ContentPlaceHolder1$ddlQ_M'
    EVENT_TARGET = '__EVENTTARGET'
    EVENT_ARGUMENT = '__EVENTARGUMENT'


class SITCAExpense:
    _TARGET_URL = 'https://www.sitca.org.tw/ROC/Industry/IN2211.aspx'

    def __init__(self, data_dir: Path = Path('data')) -> None:
        self.session = HTMLSession()
        self.sitca_data = data_dir.joinpath('sitca')
        self.file_name = 'fund-expense-{year}-{month}.json'
        self.form = {}

    def fetch_form_value(self) -> SITCAFormValue:
        res = self.session.get(self._TARGET_URL)
        sitca_form_value = self._parse_form_value(res.html)
        self.form = self._fetch_form(res.html)
        return sitca_form_value

    def fetch_data(self,
                   year: str = str(datetime.now().year),
                   month: str = 'Year',
                   save: bool = False) -> SITCAExpenseTable:
        form_value = self.fetch_form_value()
        if year not in form_value.year or month not in form_value.month:
            raise RuntimeError('arguments not in form value')
        res = self._submit(year, month)
        table = self._parse_table(res.html)
        if save:
            self._save_data(year, month, table)
        return table

    def get_table(self,
                  year: str,
                  update: bool = False,
                  **kwargs) -> SITCAExpenseTable:
        target_path = self.sitca_data.joinpath(
            self.file_name.format(year=year, month='Year'))
        if target_path.is_file():
            return SITCAExpenseTable.parse_file(target_path)
        elif update:
            return self.fetch_data(year, **kwargs)
        else:
            raise RuntimeError('file does not exist: {}'.format(target_path))

    def _fetch_form(self, html) -> Dict:
        return {i.attrs['name']: i.attrs['value'] for i in html.find('input')}

    def _parse_form_value(self, html) -> SITCAFormValue:
        def parse_value(ele) -> List[str]:
            return [o.attrs['value'] for o in ele.find('option')]

        year = html.find('#' + SITCAFormMeta.YEAR_ID.value, first=True)
        month = html.find('#' + SITCAFormMeta.MONTH_ID.value, first=True)

        return SITCAFormValue(year=parse_value(year), month=parse_value(month))

    def _submit(self, year, month):
        # post year
        logger.info('submit year field')
        self.form[SITCAFormMeta.YEAR_NAME.value] = year
        self.form[SITCAFormMeta.EVENT_TARGET.value] = SITCAFormMeta.YEAR_NAME
        self.form[SITCAFormMeta.EVENT_ARGUMENT.value] = ''
        res = self.session.post(self._TARGET_URL, data=self.form)
        res.raise_for_status()
        self.form = self._fetch_form(res.html)
        # post month
        logger.info('submit month field')
        self.form[SITCAFormMeta.MONTH_NAME.value] = month
        self.form[SITCAFormMeta.EVENT_TARGET.value] = SITCAFormMeta.MONTH_NAME
        self.form[SITCAFormMeta.EVENT_ARGUMENT.value] = ''
        res = self.session.post(self._TARGET_URL, data=self.form)
        res.raise_for_status()
        self.form = self._fetch_form(res.html)
        # submit
        logger.info('submit form')
        self.form[SITCAFormMeta.YEAR_NAME.value] = year
        self.form[SITCAFormMeta.MONTH_NAME.value] = month
        self.form[SITCAFormMeta.EVENT_TARGET.value] = ''
        self.form[SITCAFormMeta.EVENT_ARGUMENT.value] = ''
        res = self.session.post(self._TARGET_URL, data=self.form)
        res.raise_for_status()
        res.html.encoding = 'utf-8'
        return res

    def _parse_table(self, html) -> SITCAExpenseTable:
        result = SITCAExpenseTable()
        funds = html.find('table')[-1].find('tr')[3:]
        for f in funds:
            result.add_fund(create_from_sitca_expense(f.text.split('\n')))

        return result

    def _save_data(self, year: str, month: str, table: SITCAExpenseTable):
        self.sitca_data.mkdir(parents=True, exist_ok=True)
        targe_path = self.sitca_data.joinpath(
            self.file_name.format(year=year, month=month.lower()))
        with open(targe_path, 'w', encoding='utf-8') as f:
            f.write(table.json(ensure_ascii=False))
