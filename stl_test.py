
import requests

ibm=requests.get('https://www.quandl.com/api/v1/datasets/GOOG/NYSE_IBM.json?trim_start=2014-01-01&trim_end=2014-11-11')

data=map(lambda x: [x[0],x[4]],ibm.json()['data'])
ts=[float(item[1]) for item in data]
dates=[item[0] for item in data]
data2='ts(c('+str(ts)[1:-2]+'),frequency=12)' #need to post data as a time series object to stl
url='https://public.opencpu.org/ocpu/library/stats/R/stl'
params={'x':data2,'s.window':4}
r=requests.post(url,params)
#stl returns an object of class stl with components 
#time.series a multiple time series with columns seasonal, trend and remainder.
#weights	the final robust weights (all one if fitting is not done robustly).
#$call	the matched call ... etc
#this object is not JSON-Serializable so we need to do another opencpu call to extract the time.series object

result=r.text.split('\n')[0] #gets the tmp storage address of the R object from the first request
url2='https://public.opencpu.org/ocpu/library/base/R/get/json'
params2={'x':'"time.series"','pos':result[10:21]} #using get to extract the time.series object
r2=requests.post(url2,params2)
#raw=map(lambda x: x['raw'],r2.json())
seasonal=map(lambda x: x[0],r2.json())
trend=map(lambda x: x[1],r2.json())
remainder=map(lambda x: x[2],r2.json())
raw_ts=map(lambda x:{"DateTime":x[0],"Value":x[1]},zip(dates,ts))
seasonal_ts=map(lambda x:{"DateTime":x[0],"Value":x[1]},zip(dates,seasonal))
remainder_ts=map(lambda x:{"DateTime":x[0],"Value":x[1]},zip(dates,remainder))
trend_ts=map(lambda x:{"DateTime":x[0],"Value":x[1]},zip(dates,trend))

stl={'raw':raw_ts,'seasonal':seasonal_ts,'trend':trend_ts,'remainder':remainder_ts}
json.dumps(stl)





