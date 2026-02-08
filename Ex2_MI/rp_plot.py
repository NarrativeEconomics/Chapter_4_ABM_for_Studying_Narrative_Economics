# recurrence plot for BSE1-PZRI

import csv
import sys
import os
import math
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

plt.close('all')



default_csv_fname = "bse_MI_min150_i05_0001_strats.csv"
sess_id = ': BFL-PRDE'


# time is converted internally from seconds to days when reading in csv
start_t = 0
end_t = False   # if false then continue until end of file.
# end_t = 300     # 300 days

plot_strat_lines = True
csv_dump_strats = False

plot_strat_heat = True
csv_dump_heat = False

plot_profits = True
csv_dump_profits = True

plot_rp = False
csv_dump_rp = False
analyse_rp = False

# how many csv columns per trader record
record_len = 7

if __name__ == "__main__":


    argc = len(sys.argv) # has to do with the number of files we are processing

    if argc < 2:
        argv = [default_csv_fname]
        # argv = ['test01.csv', 'test02.csv']

    else:
        argv = sys.argv[1:]
    #print("--------------------------------------------", argv) # argv = ['bse_d050_i05_0002_strats.csv']
    #print('Processing %d csv files' % len(argv))

    for csv_fname in argv:
        # we're not doing any checks on the filenames -- errors => crashes

        #print('Processing csv file: %s' % csv_fname)

        sess_id = ': ' + csv_fname[:-4]
        # first pass through the whole data file: how many rows? how many buyers, how many sellers?

        #print("csv_fname = ", csv_fname)
        with open(csv_fname) as csvfile: #Read the file

            n_rows = 0
            first_row = True
            for row in csv.reader(csvfile):
                # first pass thru the file to find how many buyers & sellers per row, and how many rows
                if first_row:
                    # this is the first row we've seen -- find out how many buyers and sellers
                    #print(row)
                    n_buyers = 0
                    n_sellers = 0
                    reading_buyers = True
                    id_index = 3 # beacuse the trader name is on the 4th coloumn
                    while id_index < len(row):
                        id_str = row[id_index]
                        if reading_buyers and id_str[0] == 'B': # the first letter is B
                            n_buyers += 1
                        elif id_str[0] == 'S': # we reached  the sellers
                            reading_buyers = False
                            n_sellers += 1
                        elif not reading_buyers and id_str[0] == 'B': #  this the last coloumns
                            # this is the best buyer, a duplicate from the original list of all buyers
                            break
                        else:
                            print('HUH??? %s, ' % row[id_index])
                            sys.exit()
                        id_index += record_len
                    #print('Found %d buyers and %d sellers' % (n_buyers, n_sellers))
                    first_row = False

                n_rows += 1 # go to the next row

            #print('Found %d rows\n' % n_rows)


        # rp_data holds the data for the recurrence plot: we're going to grow it line by line
        rp_data = []

        with open(csv_fname) as csvfile:

            # buyer/seller strategy data
            b_strat_data = []
            s_strat_data = []

            # buyer/seller profit data
            b_profit_data = []
            s_profit_data = []

            # total profit
            t_profit_data = []

            # RP data
            s_rp_data = []
            b_rp_data = []

            row_count = 0

            for row in csv.reader(csvfile):

                # second pass: read in the buyer and seller strategies, and sort them
                time = float(row[1])/(60*60*24) # convert seconds to days

                if end_t is not False:
                    if time > end_t:
                        break

                row_count += 1

                b_strats = []
                s_strats = []
                b_profits = []
                s_profits = []
                t_profits = []

                # BUYER DATA

                # gather the profit data
                b_row_profit = 0.0
                first_buyer_prof = 8 # the ninth coloumn in the file

                for buyer_i in range(n_buyers):
                    profit = float(row[first_buyer_prof + (buyer_i * record_len)])
                    b_row_profit += profit  # sum all porfits
                    b_profits.append(profit)

                print('b_profits= %s' % b_profits)
                #print('b_row_profit= %f' % b_row_profit)

                b_prof_data_row = [float(time), b_row_profit]
                b_profit_data.append(b_prof_data_row)

                # gather the strategy data
                first_buyer_strat = 6 # seventh cloulomn
                for buyer_i in range(n_buyers):
                    b_strats.append(float(row[first_buyer_strat + (buyer_i * record_len)]))
                #print('b_strats= %s' % b_strats)
                bs_sorted = sorted(b_strats)
                #print('bs_sorted= %s' % bs_sorted)

                b_strat_data_row = [float(time)]
                for strat in b_strats:
                    b_strat_data_row.append(strat)
                b_strat_data.append(b_strat_data_row)

                b_rp_data_row = [float(time)]
                for strat in bs_sorted:
                    b_rp_data_row.append(strat)
                b_rp_data.append(b_rp_data_row)


                # SELLER DATA

                # gather the profit data
                s_row_profit = 0.0
                first_seller_prof = first_buyer_prof + (n_buyers * record_len)
                for seller_i in range(n_sellers):
                    index = first_seller_prof + (seller_i * record_len)
                    rowentry = row[index]
                    #print('%d %s' % (index, rowentry))
                    sys.stdout.flush()
                    profit = float(row[first_seller_prof + (seller_i * record_len)])
                    s_row_profit += profit
                    s_profits.append(profit)
                #print('s_profits= %s' % s_profits)
                #print('s_row_profit= %f' % s_row_profit)

                s_prof_data_row = [float(time), s_row_profit]
                s_profit_data.append(s_prof_data_row)

                t_row_profit = b_row_profit + s_row_profit
                print('t_row_profit= %f' % t_row_profit)
                t_prof_data_row = [float(time), b_row_profit, s_row_profit, t_row_profit]
                t_profit_data.append(t_prof_data_row)


                first_seller_strat = first_buyer_strat + (n_buyers * 7) # 6 + (n_buyers * no of coloumns)
                #print("first_seller_strat", first_seller_strat)
                #print("s_strats",s_strats)
                #print("(seller_i * record_len",(seller_i * record_len))

                for seller_i in range(n_sellers):

                    s_strats.append(float(row[first_seller_strat + (seller_i * record_len)]))
                    #print("-----------------------",(row[first_seller_strat + (seller_i * record_len)]))
                    #s_strats.append(float(row[first_seller_strat + (seller_i * record_len)]))

                #print('s_strats= %s' % s_strats)

                ss_sorted = sorted(s_strats)
                #print('ss_sorted= %s' % ss_sorted)

                s_strat_data_row = [float(time)]

                for strat in s_strats:
                    s_strat_data_row.append(strat)

                s_strat_data.append(s_strat_data_row)

                s_rp_data_row = [float(time)]

                for strat in ss_sorted:
                    s_rp_data_row.append(strat)
                #print('s_rp_data_row=%s' % s_rp_data_row)

                s_rp_data.append(s_rp_data_row)



        # frame the data
        print("before smothing", b_strat_data)
        bsdf = pd.DataFrame(b_strat_data)

        ssdf = pd.DataFrame(s_strat_data)
        print("###############################################", ssdf)

        bpdf = pd.DataFrame(b_profit_data)
        spdf = pd.DataFrame(s_profit_data)

        tpdf = pd.DataFrame(t_profit_data)
        tpdf = tpdf.set_axis(['time', 'B-profit', 'S-Profit', 'Sum'], axis=1)

        # smooth the frames
        #n_hours = 60*60*24 * 5
        n_hours = 24

        smth_bsdf = bsdf.rolling(n_hours).sum()/n_hours
        print("##################### after ##########################", smth_bsdf)


        smth_ssdf = ssdf.rolling(n_hours).sum()/n_hours

        smth_bpdf = bpdf.rolling(n_hours).sum()/n_hours
        smth_spdf = spdf.rolling(n_hours).sum()/n_hours
        smth_tpdf = tpdf.rolling(n_hours).sum()/n_hours

        # dump as csv?
        if csv_dump_profits:
            fname = sess_id[2:] + '_profits.csv'
            smth_tpdf.to_csv(fname, encoding='utf-8', index=False)

        # now we can plot strat-vs-time graphs
        sess_id = ': BFL-PRDE'
        xrange = (0, 15)

        plt.figure()

        # line graphs

        if plot_strat_lines:
            smth_bsdf.plot(title='Buyer Strategies'+sess_id, x=0, legend=False, color='black', lw=0.25)
            plt.xlabel('Day')
            plt.ylabel('Strategy Value')
            plt.show()

            plt.figure()
            smth_ssdf.plot(title='Seller Strategies'+sess_id, x=0, legend=False, color='black', lw=0.25)
            plt.xlabel('Day')
            plt.ylabel('Strategy Value')
            plt.show()

        if plot_profits:
            plt.figure()
            ax = smth_tpdf.plot(title='Profit'+sess_id, x=0, legend=True, lw=0.75)
            plt.xlabel('Day')
            plt.ylabel('Profit per Second')
            plt.show()


        #convert dataframe to Nx2

        plt.figure()
        frames = []
        for b in range(1, n_buyers + 1):
                buyercol = bsdf[[0, b]]
                buyercol = buyercol.set_axis(['time','strat'], axis=1)
                print(b, buyercol)
                frames.append(buyercol)
        allframes = pd.concat(frames)
        #print(allframes)

        n_days=50



        # 2d histogram
        # sns.kdeplot(x=allframes['time'], y=allframes['strat'], cmap='Reds', shade=True, bw_adjust=0.5)
        plt.hist2d(density=True, x=allframes['time'], y=allframes['strat'], bins=(n_days, 50), cmap=plt.cm.Reds)
        plt.colorbar()
        plt.title('Buyer Strategies'+sess_id)
        plt.xlabel('Day')
        plt.ylabel('Strategy Value')
        plt.show()

        plt.figure()
        frames = []
        for s in range(1, n_sellers + 1):
                sellercol = ssdf[[0, s]]
                sellercol = sellercol.set_axis(['time','strat'], axis=1)
                print(s, sellercol)
                frames.append(sellercol)
        allframes = pd.concat(frames)
        #print(allframes)

        # 2d histogram
        # sns.kdeplot(x=allframes['time'], y=allframes['strat'], cmap='Reds', shade=True, bw_adjust=0.5)
        plt.hist2d(density=True, x=allframes['time'], y=allframes['strat'], bins=(n_days, 50), cmap=plt.cm.Reds)
        plt.colorbar()
        plt.title('Seller Strategies'+sess_id)
        plt.xlabel('Day')
        plt.ylabel('Strategy Value')
        plt.show()

        # at this stage we have b_rp_data and s_rp_data fully loaded,
        # now we need to loop through them to record recurrence data

        start = 0           # what row to start with
        end = row_count     # what row to end with (max=n_rows)
        # end = 24*7
        row_steps = 10  # calculate recurrence once every row_steps rows (smaller row_steps => bigger pixel-count

        rp_data = []
        for row in range(start, end, row_steps):
            # for the data at this row, compute distance to all other times, i.e. across all columns
            rp_row = []

            row_strats = b_rp_data[row][1:] + s_rp_data[row][1:]
            lrs = len(row_strats)

            # thrsh_dist is threshold distance for binarization
            # NB it's much quicker to compare squares of distances (cuts out calls to sqrt)
            dist_each_strat = 0.05
            thrsh_dist_sq = lrs * (dist_each_strat * dist_each_strat)
            max_dist_sq = lrs * (2*2)
            # thrsh_dist = math.sqrt(thrsh_dist_sq)

            # print('row=%d, strats=%s' % (row, row_strats))
            #print('%s -- row=%d ' % (sess_id, row))
            for col in range(start, end, row_steps):
                col_strats = b_rp_data[col][1:] + s_rp_data[row][1:]
                # calculate distance
                sumsq = 0.0
                for i in range(lrs):
                    delta = row_strats[i] - col_strats[i]
                    sumsq += delta * delta
                dist_sq = sumsq
                # dist = math.sqrt(sumsq)
                if dist_sq < thrsh_dist_sq:
                    dist = 0.0
                else:
                    dist = 1.0
                rp_row.append(dist)
                # rp_row.append(dist_sq/max_dist_sq)
            rp_data.append(rp_row)

        # right now we have un-normalized distance data


        rp_arr = np.array(rp_data)

        # plt.imshow(rp_arr, interpolation='nearest', cmap='gray', origin='lower')
        # plt.show()
        # plt.imsave(csv_fname + '_full.png', rp_arr, cmap='gray', origin='lower')

        fig, ax = plt.subplots()

        c = ax.imshow(rp_arr, cmap='gray',
                      interpolation='nearest',
                      origin='lower')
        # fig.colorbar(c, ax=ax)
        ax.set_title('RP' + sess_id)
        plt.show()


        # now for some RQA...

        # calculate frequency distribution for vertical lines in upper-diagonal

        # we're going to delete active cells from a copy of the RP
        rp_edit = np.copy(rp_arr)

        # vertical-line frequency distribution starts out as an empty dictionary
        vlfd = {}

        def vert_freq_dist_update(vlfd_dict, vl_len):
            vl_len_str = str(vl_len)
            if vl_len_str in vlfd_dict:
                # not the first vertical line of this length, so update counter
                vl_len_count = vlfd_dict[vl_len_str]
                vlfd_dict[vl_len_str] = vl_len_count + 1
            else:
                # first time we've seen a line of this length, so count is one
                vlfd_dict[vl_len_str] = 1
            #print(vlfd_dict)

        # count vertical lines of all lengths >=1
        n_rows = rp_edit.shape[0]
        for row in range(n_rows):
            for col in range(n_rows):
                print('%d %d: %d' % (row, col, rp_edit[row, col]
                                     ))
                if row == rp_edit.shape[0]:
                    # special case for top row: nothing above
                    if rp_edit[row, col] == 0:
                        vert_freq_dist_update(vlfd, 1)
                        rp_edit[row, col] = 1
                else:
                    # at least one pixel above, so start count here and go vertical
                    if rp_edit[row, col] == 0:
                        vcount = 1
                        rp_edit[row, col] = 1
                        c = col + 1
                        while c < rp_edit.shape[1] and rp_edit[row, c] == 0:
                            vcount += 1
                            rp_edit[row, c] = 1
                            c += 1
                        vert_freq_dist_update(vlfd, vcount)

        # print the edited RP to check everything was counted
        # plt.imshow(rp_edit, interpolation='nearest', cmap='gray', origin='lower')
        # plt.show()

        # now we have the vertical-line length freq distbn we can calculate Laminarity and Traopping Time

        vPv_1 = 0
        for v in range(rp_edit.shape[0]):
            if str(v) in vlfd:
                vfreq = vlfd[str(v)]
                vPv_1 += v * vfreq
        print('vPv_1 %d' % vPv_1)

        v_min = 2
        vPv_vmin = 0
        for v in range(v_min, rp_edit.shape[0]):
            if str(v) in vlfd:
                vfreq = vlfd[str(v)]
                vPv_vmin += v * vfreq
        print('vPv_min %d' % vPv_vmin)

        lam = vPv_vmin / vPv_1
        print('Laminarity = %f' % lam)

        Pv_vmin = 0
        for v in range(v_min, rp_edit.shape[0]):
            if str(v) in vlfd:
                vfreq = vlfd[str(v)]
                Pv_vmin += vfreq
        print('Pv_min %d' % Pv_vmin)

        if Pv_vmin > 0:
            tt = vPv_vmin / Pv_vmin
            print('TrappingTime = %f' % tt)
        else:
            print('Trapping Time undefined because Pv_vmin=0')
