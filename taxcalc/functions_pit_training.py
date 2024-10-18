"""
pitaxcalc-demo functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit

"Calculation for exemption for the disabled"
@iterate_jit(nopython=True)
def cal_exemption_amt(EXEMPTION_AMT, IS_EXEMPT_CERT_PRSNT_1, EXEMPTION_CLAIMED):
    if (IS_EXEMPT_CERT_PRSNT_1==1):
        EXEMPTION_CLAIMED = EXEMPTION_AMT
    else:
        EXEMPTION_CLAIMED = 0
    return EXEMPTION_CLAIMED

"Calculation for mortgage interest"
@iterate_jit(nopython=True)
def cal_mortgage_interest(MORTAGE_INTEREST,MORTAGE_INTEREST_CLAIMED):
    if(MORTAGE_INTEREST<=300000):
        MORTAGE_INTEREST_CLAIMED = 0.15*MORTAGE_INTEREST
    else:
        MORTAGE_INTEREST_CLAIMED = 0.15*300000
    return MORTAGE_INTEREST_CLAIMED

"Calculation for insurance relief"
@iterate_jit(nopython=True)
def cal_insurance_relief(INSURANCE_RELIEF_LIMIT, INSURANCE_RELIEF,INSURANCE_RELIEF_ALLOWED):
    if(INSURANCE_RELIEF<=INSURANCE_RELIEF_LIMIT):
        INSURANCE_RELIEF_ALLOWED = INSURANCE_RELIEF
    else:
        INSURANCE_RELIEF_ALLOWED = INSURANCE_RELIEF_LIMIT
           
    return INSURANCE_RELIEF_ALLOWED

"Calculation for net taxable income"
@iterate_jit(nopython=True)
def cal_taxable_income(CHARGEABLE_INCOME, MORTAGE_INTEREST_CLAIMED, EXEMPTION_CLAIMED, NTI):
    NTI = CHARGEABLE_INCOME - MORTAGE_INTEREST_CLAIMED - EXEMPTION_CLAIMED
    return NTI


"Calculation for PIT from wages only"
@iterate_jit(nopython=True)
def cal_pit_w( rate1, rate2, rate3, rate4, rate5, tbrk1, tbrk2, tbrk3, tbrk4, NTI, pit_w):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given net taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = NTI  
    
    pit_w = (rate1 * min(taxinc, tbrk1) +
                    rate2 * min(tbrk2 - tbrk1, max(0., taxinc - tbrk1)) +
                    rate3 * min(tbrk3 - tbrk2, max(0., taxinc - tbrk2)) +
                    rate4 * min(tbrk4 - tbrk3, max(0., taxinc - tbrk3)) +                   
                    rate5 * max(0., taxinc - tbrk4))      
    return (pit_w)

@iterate_jit(nopython=True)
def cal_total_tax_payable(PERSONAL_RELIEF, pit_w, pitax):
    """
    Compute net income.
    """
    pitax = pit_w - PERSONAL_RELIEF
    return pitax
