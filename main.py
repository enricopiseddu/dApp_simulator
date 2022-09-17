from Actor import *
from Customer import *
from Operator import *
# from simulator import Simulator
from simulator import *
import os
import matplotlib.pyplot as plt
import pandas as pd
import statistics as st

# simulator creation
s = Simulator.getInstance()

# read data from files
s.getInstance().readActorsFrom('./configuration/actors.csv')
s.getInstance().readComponentsFrom('./configuration/components.csv')
s.getInstance().readTransactionsFrom('./configuration/transactions.csv')

total_actors = len(s.getInstance().actors)
print('Total actors ', total_actors)

print('\n')

print('Simulator is running...')
# we run the simulator
s.getInstance().run()
print('Simulation ended\n')

# From this point, we compute all needed outputs

# remove comment if there is not the directory named "/report"
# os.mkdir('./report')
# os.mkdir('./report/components')

for c in s.getInstance().components:
    # we take transactions from 8am to 10pm with step of 1 hour
    c.txsInInterval(28800000, 82800000, 3600000, './report/components/' + c.name + '_transactions_actors_'+ str(total_actors)+'.csv')
    df = pd.read_csv('./report/components/' + c.name + '_transactions_actors_' + str(total_actors)+'.csv', sep=',')
    df.plot(x='time', y=['started', 'ended'])
    plt.ylabel('transactions')
    plt.title('Component: ' + c.name + '\nTotal actors:' + str(total_actors))
    plt.grid()
    plt.savefig('./report/components/' + c.name + '_transactions_actors_'+ str(total_actors)+'.png')
    plt.show()


# ************ ALL BASIC TXS STATISTICS ************
app_input = []  # txs list of "app input"
app_read = []
dlt_read = []
dlt_write = []
dltview_read = []
dms_docDown = []
dms_docUpl = []
dbms_read = []
dbms_write = []

# we collect all basic transactions in their appropriate data structure
for c in s.components:
    for tx in c.allTxs:
        typeTx = tx.type.id
        if typeTx == 'Input':
            app_input.append(tx)
        if typeTx == 'Read':
            app_read.append(tx)
        if typeTx == 'DLT_read' and c.name == 'dlt':
            dlt_read.append(tx)
        if typeTx == 'DLT_write':
            dlt_write.append(tx)
        if typeTx == 'DLT_read' and c.name == 'dltview':
            dltview_read.append(tx)
        if typeTx == 'Doc_download':
            dms_docDown.append(tx)
        if typeTx == 'Doc_upload':
            dms_docUpl.append(tx)
        if typeTx == 'DB_write':
            dbms_write.append(tx)
        if typeTx == 'DB_read':
            dbms_read.append(tx)

allTxs = [app_input, app_read, dlt_read, dlt_write, dltview_read, dms_docDown, dms_docUpl, dbms_write, dbms_read]
basicTxName = ['app_input', 'app_read', 'dlt_read', 'dlt_write', 'dltview_read', 'dms_docDown', 'dms_docUpl', 'dbms_write', 'dbms_read']

medianDuration = [0]*len(allTxs)
averageDuration = [0]*len(allTxs)
stdDevDuration = [0]*len(allTxs)
maxDuration = [0]*len(allTxs)
minDuration = [0]*len(allTxs)

i = 0  # index of basic tx
# we compute statistics for each basic transaction
for c in allTxs:
    temp_durations = []
    for tx in c:
        temp_durations.append(tx.durationInMsec())

    medianDuration[i] = st.median(temp_durations)
    averageDuration[i] = st.mean(temp_durations)
    stdDevDuration[i] = st.stdev(temp_durations)
    maxDuration[i] = max(temp_durations)
    minDuration[i] = min(temp_durations)
    i += 1


# we generate a .csv file with statistics for each basic transaction
f = open('./report/base_txs_duration_statistics_actors_'+ str(total_actors)+'.csv', 'w')
f.write('base_tx_name,avg,median,stdDev,max,min\n')

i = 0
for c in allTxs:
    f.write(str(basicTxName[i]) + ',' + str(averageDuration[i]) + ',' + str(medianDuration[i])+ ',' + str(stdDevDuration[i])+ ',' + str(maxDuration[i])+ ',' + str(minDuration[i]) + '\n')
    i += 1
f.close()


d = pd.read_csv('./report/base_txs_duration_statistics_actors_' + str(total_actors)+'.csv')
x = [1,2,3,4,5,6,7,8,9]
avgDur = d['avg']

plt.bar(x, avgDur, align='center')
plt.xticks(x, basicTxName)
plt.xticks(rotation=45, fontsize=5.5)
plt.title('Average of duration of basic transactions\nTotal actors: ' + str(total_actors))
plt.ylabel('time in ms')
plt.grid(axis='y')
plt.savefig('./report/base_txs_duration_actors_' + str(total_actors)+'.png')
plt.show()


# ****** STATISTIC OF BASE TXS IN A GIVEN TIME INTERVAL
app_input = []  # txs list of "app input"
app_read = []
dlt_read = []
dlt_write = []
dltview_read = []
dms_docDown = []
dms_docUpl = []
dbms_read = []
dbms_write = []

start_interval = 12 * 3600 * 1000  # start interval at 12.00
end_interval = 15 * 3600 * 1000  # end interval at 3pm

# we collect all basic transactions in their appropriate data structure
for c in s.components:
    for tx in c.allTxs:
        # we consider only txs started in the given interval
        if tx.creationTime in range(start_interval, end_interval):
            typeTx = tx.type.id
            if typeTx == 'Input':
                app_input.append(tx)
            if typeTx == 'Read':
                app_read.append(tx)
            if typeTx == 'DLT_read' and c.name == 'dlt':
                dlt_read.append(tx)
            if typeTx == 'DLT_write':
                dlt_write.append(tx)
            if typeTx == 'DLT_read' and c.name == 'dltview':
                dltview_read.append(tx)
            if typeTx == 'Doc_download':
                dms_docDown.append(tx)
            if typeTx == 'Doc_upload':
                dms_docUpl.append(tx)
            if typeTx == 'DB_write':
                dbms_write.append(tx)
            if typeTx == 'DB_read':
                dbms_read.append(tx)

allTxs = [app_input, app_read, dlt_read, dlt_write, dltview_read, dms_docDown, dms_docUpl, dbms_write, dbms_read]
basicTxName = ['app_input', 'app_read', 'dlt_read', 'dlt_write', 'dltview_read', 'dms_docDown', 'dms_docUpl', 'dbms_write', 'dbms_read']

medianDuration = [0]*len(allTxs)
averageDuration = [0]*len(allTxs)
stdDevDuration = [0]*len(allTxs)
maxDuration = [0]*len(allTxs)
minDuration = [0]*len(allTxs)
i = 0

# we compute statistics for each basic transaction
for c in allTxs:
    temp_durations = []
    for tx in c:
        temp_durations.append(tx.durationInMsec())

    medianDuration[i] = st.median(temp_durations)
    averageDuration[i] = st.mean(temp_durations)
    stdDevDuration[i] = st.stdev(temp_durations)
    maxDuration[i] = max(temp_durations)
    minDuration[i] = min(temp_durations)
    i += 1


# we generate a .csv file with statistics for each basic transaction
f = open('./report/interval_base_txs_duration_statistics_actors_'+ str(total_actors)+'.csv', 'w')
f.write('base_tx_name,avg,median,stdDev,max,min\n')

i = 0
for c in allTxs:
    f.write(str(basicTxName[i]) + ',' + str(averageDuration[i]) + ',' + str(medianDuration[i])+ ',' + str(stdDevDuration[i])+ ',' + str(maxDuration[i])+ ',' + str(minDuration[i]) + '\n')
    i += 1
f.close()


d = pd.read_csv('./report/interval_base_txs_duration_statistics_actors_' + str(total_actors)+'.csv')
x = [1,2,3,4,5,6,7,8,9]
avgDur = d['avg']

plt.bar(x, avgDur, align='center')
plt.xticks(x, basicTxName)
plt.xticks(rotation=45, fontsize=5.5)
plt.title('Average of duration of basic transactions in the given interval\nTotal actors: ' + str(total_actors))
plt.ylabel('time in ms')
plt.grid(axis='y')
plt.savefig('./report/interval_base_txs_duration_actors_' + str(total_actors)+'.png')
plt.show()


# *********** AVG DURATION OF COMPLEX TXS **************
# estimation of duration of complex transactions
complexTxsName = ['Simple Write', 'Document Write', 'Simple Read', 'Document Read']
avgDurComplexTxs = [
    averageDuration[0] + averageDuration[2] + averageDuration[3] + averageDuration[7] + averageDuration[8],  # sum of durations of basic transaction
    averageDuration[0] + averageDuration[2] + averageDuration[3] + averageDuration[6]+ averageDuration[7] + averageDuration[8],
    averageDuration[1] + averageDuration[4],
    averageDuration[1]*2 + averageDuration[4] + averageDuration[5]
]

plt.bar([1,2,3,4], avgDurComplexTxs, align='center')
plt.xticks([1,2,3,4], complexTxsName)
plt.xticks(fontsize=10)
plt.title('Average of duration of complex transactions\nTotal actors: ' + str(total_actors))
plt.ylabel('time in ms')
plt.grid(axis='y')
plt.savefig('./report/complex_txs_duration_actors_'+ str(total_actors)+'.png')
plt.show()


# ********* NR. BASIC TXS/SEC, for each component *********
print("Nr. basic tx/sec, for each component: ")
for c in s.components:
    # number of txs for the component c, except for the appSys component
    if c.name != 'appSys':
        numTxComp = len(c.allTxs)
        duration = 0
        for tx in c.allTxs:
            duration = duration + tx.duration()
        print("Component " + c.name + ": " + str(numTxComp/duration) + " tx/sec")

print('\n Other statistics and report available in ./report')
