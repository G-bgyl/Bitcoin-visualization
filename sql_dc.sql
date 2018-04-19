select max(spot_price),min(spot_price),[month]
from Coinbase
where year =2017
group by [month];

--select spot_price
--from Coinbase
--where year =2017 and [month]=1 and [day]=1;

select [date], spot_price
from Coinbase
where year =2017;

select price, volume
from Okcoin 
where type='bids';


select [month], avg(spot_price)
from Coinbase
where year =2017
group by [month];

