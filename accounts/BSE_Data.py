import pandas as pd
from bs4 import BeautifulSoup
import requests, logging
from collections import defaultdict
from datetime import datetime
import pandas


# Mapping for passing data attribute in get/post request
BSE_index_val_mapping = {
	"16" : "BSE SENSEX",
	"22" : "BSE 100",
	"23" : "BSE 200",
	"17" : "BSE 500",
	"75" : "BSE GREENEX",
	"77" : "BSE CARBONEX",
	"101" : "BSE 100 ESG Index",
	"113" : "BSE 100 LargeCap TMC Index",
	"102" : "BSE 150 MidCap Index",
	"104" : "BSE 250 LargeMidCap Index",
	"103" : "BSE 250 SmallCap Index",
	"105" : "BSE 400 MidSmallCap Index",
	"87" : "BSE AllCap",
	"42" : "BSE AUTO",
	"53" : "BSE BANKEX",
	"100" : "BSE Bharat 22 Index",
	"25" : "BSE CAPITAL GOODS",
	"88" : "BSE Commodities",
	"89" : "BSE Consumer Discretionary",
	"27" : "BSE CONSUMER DURABLES",
	"80" : "BSE CPSE",
	"111" : "BSE Diversified Financials Revenue Growth Index",
	"106" : "BSE Dividend Stability Index",
	"65" : "BSE DOLLEX 100",
	"48" : "BSE DOLLEX 200",
	"47" : "BSE DOLLEX 30",
	"90" : "BSE Energy",
	"107" : "BSE Enhanced Value Index",
	"83" : "BSE Fast Moving Consumer Goods",
	"91" : "BSE Financial Services",
	"84" : "BSE Healthcare",
	"79" : "BSE India Infrastructure Index",
	"86" : "BSE India Manufacturing Index",
	"92" : "BSE Industrials",
	"85" : "BSE Information Technology",
	"72" : "BSE IPO",
	"93" : "BSE LargeCap",
	"108" : "BSE Low Volatility Index",
	"35" : "BSE METAL",
	"81" : "BSE MidCap",
	"94" : "BSE MidCap Select Index",
	"109" : "BSE Momentum Index",
	"37" : "BSE OIL &amp; GAS",
	"69" : "BSE POWER",
	"114" : "BSE Private Banks Index",
	"44" : "BSE PSU",
	"110" : "BSE Quality Index ",
	"67" : "BSE REALTY",
	"98" : "BSE SENSEX 50",
	"99" : "BSE SENSEX Next 50",
	"121" : "BSE Services",
	"82" : "BSE SmallCap",
	"95" : "BSE SmallCap Select Index",
	"76" : "BSE SME IPO",
	"45" : "BSE TECK",
	"96" : "BSE Telecommunication",
	"97" : "BSE Utilities",
}

# BSE_Indexmap - { IndexName in BSE site : IndexRatio Profile(Stocks Model)  }
BSE_indexmap = {
	"BSE SENSEX" : "BSESENSEX",
	"BSE 100" : "BSE100",
	"BSE 200" : "BSE200",
	"BSE 500" : "BSE500",
	"BSE GREENEX" : "BSEGREENEX",
	"BSE CARBONEX" : "BSECARBONEX",
	"BSE 100 ESG Index" : "1017",
	"BSE 100 LargeCap TMC Index" : "1130",
	"BSE 150 MidCap Index" : "1177",
	"BSE 250 LargeMidCap Index" : "1181",
	"BSE 400 MidSmallCap Index" : "1182",
	"BSE AllCap" : "BSEALLCAP",
	"BSE AUTO" : "BSEAUTO",
	"BSE BANKEX" : "BSEBANKEX",
	"BSE Bharat 22 Index" : "1016",
	"BSE CAPITAL GOODS" : "BSECG",
	# "88" : "BSE Commodities",
	"BSE Consumer Discretionary" : "BSECDGS",
	"BSE CONSUMER DURABLES" : "BSECD",
	"BSE CPSE" : "S&PBSECPSE",
	"BSE Diversified Financials Revenue Growth Index" : "1188",
	"BSE Dividend Stability Index" : "1183",
	"BSE DOLLEX 100" : "BSEDOLLEX100",
	"BSE DOLLEX 200" : "BSEDOLLEX200",
	"BSE DOLLEX 30" : "BSEDOLLEX30",
	"BSE Energy" : "BSEENERGY",
	"BSE Enhanced Value Index" : "1184",
	# "83" : "BSE Fast Moving Consumer Goods",
	"BSE Financial Services": "BSEFINANCE",
	"BSE Healthcare" : "BSEHEALTHCARE",
	"BSE India Infrastructure Index" : "S&PBSEINFRA",
	"BSE India Manufacturing Index" : "BSEMFG",
	"BSE Industrials" : "BSEINDUSTRIALS",
	"BSE Information Technology" : "BSEIT",
	"BSE IPO" : "BSEIPO",
	"BSE LargeCap" : "BSELARGECAP",
	"BSE Low Volatility Index" : "1185",
	"BSE METAL" : "BSEMETAL",
	"BSE MidCap" : "BSEMIDCAP",
	"BSE MidCap Select Index" : "BSEMDSI",
	"BSE Momentum Index" : "1186",
	"BSE OIL &amp; GAS" : "BSEOIL&GAS",
	"BSE POWER" : "BSEPOWER",
	"BSE Private Banks Index" : "1018",
	"BSE PSU" : "BSEPSU",
	"BSE Quality Index " : "1187",
	"BSE REALTY" : "BSEREALTY",
	"BSE SENSEX 50" : "1125",
	"BSE SENSEX Next 50" : "1014",
	# "121" : "BSE Services",
	"BSE SmallCap" : "BSESMALLCAP",
	"BSE SmallCap Select Index" : "BSESMSI",
	"BSE SME IPO" : "BSESMEIPO",
	"BSE TECK" : "BSETECK",
	"BSE Telecommunication" : "BSETELECOM",
	"BSE Utilities" : "BSEUTILITIES",
}

# Headers to send request to get cookies and updated headers from BSE KEYSTATS INDEX
headers = {
		'authority': 'www.bseindia.com',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
		'cache-control': 'max-age=0',
		'content-type': 'application/x-www-form-urlencoded',
		# 'cookie': '_ga=GA1.1.389147366.1697012113; _ga_V1TD4QKFTR=GS1.1.1714036580.2.0.1714036580.60.0.0; _ga_TM52BJH9HF=GS1.1.1716290740.12.1.1716293599.0.0.0; RT="z=1&dm=bseindia.com&si=69125e70-3dac-4412-8390-5355b7e67a24&ss=lwg6kb2r&sl=j&tt=bt7&obo=6&rl=1&nu=37pjrufh&cl=6bxmc&ld=6bxmz&r=hmxdhb6&ul=6bxmz"',
		'origin': 'https://www.bseindia.com',
		'referer': 'https://www.bseindia.com/markets/keystatics/Keystat_index.aspx',
		'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Linux"',
		'sec-fetch-dest': 'document',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-user': '?1',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
	}

class BSE_Index_Ratio:
	def __init__(self):
		self.url = "https://www.bseindia.com/markets/keystatics/Keystat_index.aspx"
		self.headers = headers
		self.cookies = {
			'_ga': 'GA1.1.389147366.1697012113',
			'_ga_V1TD4QKFTR': 'GS1.1.1714036580.2.0.1714036580.60.0.0',
			'_ga_TM52BJH9HF': 'GS1.1.1716290740.12.1.1716293599.0.0.0',
			'RT': '"z=1&dm=bseindia.com&si=69125e70-3dac-4412-8390-5355b7e67a24&ss=lwg6kb2r&sl=j&tt=bt7&obo=6&rl=1&nu=37pjrufh&cl=6bxmc&ld=6bxmz&r=hmxdhb6&ul=6bxmz"',
		}


	def fetch_initial_data(self):
		# to get headers and cookies
		response = requests.post(
			self.url,
			headers=self.headers,
			cookies = self.cookies
		)
		self.headers = response.headers
		cookies_jar = response.cookies
		self.cookies = cookies_jar.get_dict()
	def use_case(self):
		print(self.headers)
		print("Cookies: ",self.cookies)
	def data_fetch(self):
		all_data=[]
		for index in BSE_index_val_mapping:
			data = {
				'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$gvYearwise$ctl02$lnkmonth',
				'__EVENTARGUMENT': '',
				'__VIEWSTATE': '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',
				'__VIEWSTATEGENERATOR': '6903EFD9',
				'__VIEWSTATEENCRYPTED': '',
				'__EVENTVALIDATION': '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',
				'ctl00$ContentPlaceHolder1$ddltype': index,
				# AVAILABLE YEARS = 1998 , For most of the index - data available from January 2011 to till date
				'ctl00$ContentPlaceHolder1$gvYearwise$ctl02$hdnYear': "2023",
				'ctl00$ContentPlaceHolder1$gvYearwise$ctl02$hdnMonth': "12",
		        }
			try:
				response = requests.post(
    		        'https://www.bseindia.com/markets/keystatics/Keystat_index.aspx',
    		        # cookies=cookies,
    		        headers=headers,
    		        data=data,
			        timeout=(30,30) # 30 seconds for connection, 30 seconds for reading response
			        )
				soup = BeautifulSoup(response.content, "lxml")
				daywise_table = soup.find(attrs={'id': 'ContentPlaceHolder1_grddaily'})
				tables = pd.read_html(str(daywise_table))
				table = tables[0]
				columns_to_keep = ['DATE','PE Ratios', 'PB Ratios', 'Dividend Yield']
				df = table[columns_to_keep]
				dd = defaultdict(list)
				fetched_data = df.to_dict('records', into=dd)
				first_row = fetched_data[-1]
				single_index_data = {BSE_index_val_mapping[index]: first_row}
				all_data.append(single_index_data)
			except:
				print(index, 'Table not found for this year')
		print(all_data)
		data1 = all_data[0]['BSE SENSEX']['PE Ratios'] # 0th Index for the first incex value and '16' index key name
		for item in all_data:
			for key, series in item.items():
				print(f"Index: {key}")
				print(f"Date: {series['DATE']}")
				print(f"PE Ratios: {series['PE Ratios']}")
				print(f"PB Ratios: {series['PB Ratios']}")
				print(f"Dividend Yield: {series['Dividend Yield']}")
				print('----')

		print(response.status_code)
		

obj = BSE_Index_Ratio()
obj.fetch_initial_data()
obj.use_case()