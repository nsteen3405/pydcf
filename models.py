def base_income(self, base_rate, rsf, esc, term, term_type='mo', \
  calc_basis='psf/yr', pmt_sched='mo', esc_sched='yr'):
    '''returns numpy array of base rent income'''
    term = term * term_types[term_type] # term in mos
      # psf/yr, psf/qtr, psf/mo, amt/yr, amt/qtr, amt/mo
    calc_multiplier = rent_units[calc_basis][0] # to the 1
    rsf_multiplier = rsf ** calc_multiplier
    #BASE RENT#
    if calc_basis[3:] == '/yr':
        if pmt_sched == 'mo':
            br_cf = [base_rate / 12 * rsf_multiplier for month \
              in range(12)]
        elif pmt_sched == 'qtr': #TODO: own method
            br_cf = [base_rate / 4 * rsf_multiplier for quarter \
              in range(4)]
            for quarter in range(4):
                for no_income in range(2):
                    br_cf.insert(1 + quarter * 3, 0)
        else: #i.e. pmt_sched == yearly
            br_cf = [base_rate * rsf_multiplier]
            for no_income in range(11):
                br_cf.append(0)
    elif calc_basis[3:] == '/qtr':
        if pmt_sched == 'mo':
            br_cf = [base_rate / 3 * rsf_multiplier for month \
              in range(12)]
        elif pmt_sched == 'qtr':
            br_cf = [base_rate for qtr in range(4)]
            for quarter in range(4):
                for no_income in range(2):
                    br_cf.insert(1 + quarter * 3, 0)
        else:
            br_cf = [base_rate * 4]
            for no_income in range(11):
                br_cf.append(0)
    else: #calc_basis[3:] == 'mo'
        if pmt_sched == 'mo':
            br_cf = [base_rate * rsf_multiplier for month \
              in range(12)]
        elif pmt_sched == 'qtr':
            br_cf = [base_rate * 3 * rsf_multiplier for quarter \
              in range(4)]
            for quarter in range(4):
                for no_income in range(2):
                    br_cf.insert(1 + quarter * 3, 0)
        else:
            br_cf = [base_rate * 12]
            for no_income in range(11):
                br_cf.append(0)
    #TERM#
    one_year = br_cf[:12]
    for year in range(int(term / 12)+ 1):
        br_cf += one_year
    br_cf = br_cf[:term]
    #ESCALATIONS#
    if esc_sched == 'yr':
        escalation_schedule = np.array([(1 + esc) ** yr for \
          yr in range(int(term / 12) + 1) for month in range(12)])
    elif esc_sched == 'qtr':
        escalation_schedule = np.array([(1 + esc) ** qtr for \
          qtr in range(int(term / 3) + 1) for qtr in range(3)])
    elif esc_sched == 'mo':
        escalation_schedule = np.array([(1 + esc) ** mo for \
          mo in range(term)])
    escalation_schedule = escalation_schedule[:term]
    br_cf = np.array(br_cf)
    br_cf = br_cf * escalation_schedule
    return br_cf
