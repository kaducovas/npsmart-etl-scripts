select 
rncname,count(*)*(select count(*) from umts_baseline.rules where lower(mo) = 'ucellhsdpa' 
and act = true 
group by mo)
from umts_configuration.ucellhsdpa
group by rncname
order by rncname

update umts_baseline.rules set act = false
where (mo,parameter) in 
(('UINTERFREQNCELL','CIOOFFSET'),
('UINTERFREQNCELL','CLBFLAG'),
('UINTERFREQNCELL','DRDORLDRFLAG'),
('UINTERFREQNCELL','DRDTARGETULCOVERLIMITTHD'),
('UINTERFREQNCELL','DYNCELLSHUTDOWNFLAG'),
('UINTERFREQNCELL','INTERFREQADJSQHCS'),
('UINTERFREQNCELL','INTERNCELLQUALREQFLAG'),
('UINTERFREQNCELL','MBDRFLAG'),
('UINTERFREQNCELL','MBDRPRIO'),
('UINTERFREQNCELL','NPRIOFLAG'),
('UINTERFREQNCELL','TPENALTYHCSRESELECT'),
('UINTERFREQNCELL','UINTERNCELLSRC'))


