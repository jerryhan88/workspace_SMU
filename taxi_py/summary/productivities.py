from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import individual_detail_dir
from supports._setting import HOUR, CENT, PROD_LIMIT
from supports.handling_pkl import save_pickle_file
#
import pandas as pd
#
def run():
    Y09_general = pd.read_csv('%s/Y09-individual-general.csv' % (individual_detail_dir))
    Y10_general = pd.read_csv('%s/Y10-individual-general.csv' % (individual_detail_dir))
    Y09_prev_in = pd.read_csv('%s/Y09-individual-prev-in-ap.csv' % (individual_detail_dir))
    Y10_prev_in = pd.read_csv('%s/Y10-individual-prev-in-ap.csv' % (individual_detail_dir))
    Y09_prev_out = pd.read_csv('%s/Y09-individual-prev-out-ap.csv' % (individual_detail_dir))
    Y10_prev_out = pd.read_csv('%s/Y10-individual-prev-out-ap.csv' % (individual_detail_dir))
    #
    Y09_general = Y09_general[(Y09_general['total-prod'] < PROD_LIMIT)]
    Y10_general = Y10_general[(Y10_general['total-prod'] < PROD_LIMIT)]
    Y09_prev_in = Y09_prev_in[(Y09_prev_in['ap-prod'] < PROD_LIMIT)]
    Y10_prev_in = Y10_prev_in[(Y10_prev_in['ap-prod'] < PROD_LIMIT)]
    Y09_prev_out = Y09_prev_out[(Y09_prev_out['ap-prod'] < PROD_LIMIT)]
    Y10_prev_out = Y10_prev_out[(Y10_prev_out['ap-prod'] < PROD_LIMIT)]
    # both years
    Y09_general_did, Y10_general_did = set(Y09_general['did']), set(Y10_general['did'])
    general_both_years_full_drivers = Y09_general_did.intersection(Y10_general_did)
    Y09_prev_in_did, Y10_prev_in_did = set(Y09_prev_in['did']), set(Y10_prev_in['did'])
    prev_in_both_years_full_drivers = Y09_prev_in_did.intersection(Y10_prev_in_did)
    Y09_prev_out_did, Y10_prev_out_did = set(Y09_prev_out['did']), set(Y10_prev_out['did'])
    prev_out_both_years_full_drivers = Y09_prev_out_did.intersection(Y10_prev_out_did)
    subset_drivers = general_both_years_full_drivers.intersection(prev_in_both_years_full_drivers)
    subset_drivers = list(subset_drivers.intersection(prev_out_both_years_full_drivers)) 
    #
    Y09_general = Y09_general[Y09_general['did'].isin(subset_drivers)]
    Y10_general = Y10_general[Y10_general['did'].isin(subset_drivers)]
    Y09_prev_in = Y09_prev_in[Y09_prev_in['did'].isin(subset_drivers)]
    Y10_prev_in = Y10_prev_in[Y10_prev_in['did'].isin(subset_drivers)]
    Y09_prev_out = Y09_prev_out[Y09_prev_out['did'].isin(subset_drivers)]
    Y10_prev_out = Y10_prev_out[Y10_prev_out['did'].isin(subset_drivers)]
    #
    Y09_general_gb, Y10_general_gb = Y09_general.groupby(['did']), Y10_general.groupby(['did'])
    Y09_driver_general_prod = Y09_general_gb.mean()['total-prod'].to_frame('avg_total_prod').reset_index()
    Y10_driver_general_prod = Y10_general_gb.mean()['total-prod'].to_frame('avg_total_prod').reset_index()
    Y09_driver_genprod_hour = {did : total_prod * HOUR / CENT for did, total_prod in Y09_driver_general_prod.values}
    Y10_driver_genprod_hour = {did : total_prod * HOUR / CENT for did, total_prod in Y10_driver_general_prod.values}
    #
    Y09_prev_in_gb, Y10_prev_in_gb = Y09_prev_in.groupby(['did']), Y10_prev_in.groupby(['did'])
    Y09_prev_in_driver_ap_prod = Y09_prev_in_gb.mean()['ap-prod'].to_frame('avg_ap_prod').reset_index()
    Y10_prev_in_driver_ap_prod = Y10_prev_in_gb.mean()['ap-prod'].to_frame('avg_ap_prod').reset_index()
    Y09_pin_driver_aprod_hour = {did : ap_prod * HOUR / CENT for did, ap_prod in Y09_prev_in_driver_ap_prod.values}
    Y10_pin_driver_aprod_hour = {did : ap_prod * HOUR / CENT for did, ap_prod in Y10_prev_in_driver_ap_prod.values}
    #
    Y09_prev_out_gb, Y10_prev_out_gb = Y09_prev_out.groupby(['did']), Y10_prev_out.groupby(['did'])
    Y09_prev_out_driver_ap_prod = Y09_prev_out_gb.mean()['ap-prod'].to_frame('avg_ap_prod').reset_index()
    Y10_prev_out_driver_ap_prod = Y10_prev_out_gb.mean()['ap-prod'].to_frame('avg_ap_prod').reset_index()
    Y09_pout_driver_aprod_hour = {did : ap_prod * HOUR / CENT for did, ap_prod in Y09_prev_out_driver_ap_prod.values}
    Y10_pout_driver_aprod_hour = {did : ap_prod * HOUR / CENT for did, ap_prod in Y10_prev_out_driver_ap_prod.values}
    
    save_pickle_file('%s/productivities.pkl' % (individual_detail_dir),
                     [subset_drivers, Y09_driver_genprod_hour, Y10_driver_genprod_hour, Y09_pin_driver_aprod_hour, Y10_pin_driver_aprod_hour, Y09_pout_driver_aprod_hour, Y10_pout_driver_aprod_hour])

if __name__ == '__main__':
    run()
