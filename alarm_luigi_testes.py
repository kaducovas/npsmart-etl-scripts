import luigi
import os

class ftp_atae(luigi.WrapperTask):
 
    def requires(self):
        return []
 
    def output(self):
		return luigi.LocalTarget("/etl/common/alarm/log/ftp_atae.txt")
		
    def run(self):
        with self.output().open('w') as fout:
                fout.write("")
        os.system("cd /etl/scripts/; python3.4 ftp-atae-alarm.py") 
 
class ftp_2atae(luigi.WrapperTask):
 
    def requires(self):
        yield [ftp_atae()]
 
    def output(self):
		return luigi.LocalTarget("/etl/common/alarm/log/ftp_2atae.txt")
 
    def run(self):
        with self.output().open('w') as fout:
                fout.write("")
        os.system("cd /etl/scripts/; python3.4 ftp-2atae-alarm.py")    

class xslt(luigi.WrapperTask):
 
    def requires(self):
        yield [ftp_2atae()]
 
    def output(self):
		return luigi.LocalTarget("/etl/common/alarm/log/xslt.txt")
 
    def run(self):
        with self.output().open('w') as fout:
                fout.write("")
        os.system("/etl/scripts/alarm-convert.sh")    

class parser(luigi.WrapperTask):
 
    def requires(self):
        yield [xslt()]
 
    def output(self):
		return luigi.LocalTarget("/etl/common/alarm/log/parser.txt")
 
    def run(self):
		with self.output().open('w') as fout:
			fout.write("")
		os.system("cd /etl/scripts/; python3.4 parse_alarm.py")    

try:
	os.remove("/etl/common/alarm/log/parser.txt")
	os.remove("/etl/common/alarm/log/xslt.txt")
	os.remove("/etl/common/alarm/log/ftp_2atae.txt")
	os.remove("/etl/common/alarm/log/ftp_atae.txt")
except: None
	
if __name__ == '__main__':
	luigi.run(["--local-scheduler"], main_task_cls = parser)