import requests
import json


class InformalRTBInterface:
	def get_richlist(self, num: int) -> list:
		"""Return a position list of the richest humans
		Each element is a Dict with at least ('position','personName','finalWorth','estWorthPrev') keys"""
		pass

	def get_furious(self) -> list:
		"""Return a list whose elements are top 2 richest people, and elon"""
		pass

	def get_individual(self, name: str) -> dict:
		"""Return a Dict whose item is the named richest human"""
		pass



class ForbesRTB(InformalRTBInterface):

	POSITION_API = 'https://www.forbes.com/forbesapi/person/rtb/0/position/1?fields='
	DEFAULT_PARAMS = ['position','personName','finalWorth','estWorthPrev']

	def __init__(self, api: str=POSITION_API):
		#TODO: add support for adding params
		self.url = api + ','.join(self.DEFAULT_PARAMS)
		self.rtb = self._get_RTB_list() #TODO: currently empty if method fails, and shit rolls downhill

	def get_richlist(self, num: int) -> list:
		self._update_RTB()
		
		return self.rtb[:num]

	def get_furious(self) -> list:
		self._update_RTB()
		elon = self._get_by_name('Elon Musk')
		
		return self.rtb[:2] + [elon]
	
	def get_individual(self, name: str) -> dict:
		self._update_RTB()
		
		return self._get_by_name(name)


	def _get_RTB_list(self) -> list:
		dalist = []
		r = requests.get(self.url)

		if r.status_code == 200:
			data = json.loads(r.text)
			dalist = data.get('personList', {}).get('personsLists', [])					
		
		if not dalist:
			#TODO: add error checking and method to handle when API down or they change schema
			pass
		else:
			dalist = self._billionize(dalist)

		return dalist
	
	def _update_RTB(self) -> None:
		#TODO: add functionality to only update if rtb is stale and don't overwrite with a fail, for now just get it again
		self.rtb = self._get_RTB_list()

	# forbes values are in millions, we wan't billions
	def _billionize(self, rtblist: list) -> list:
		for person in rtblist:
			person['finalWorth'] = person.get('finalWorth', 0) / 1000
			person['estWorthPrev'] = person.get('estWorthPrev', 0) / 1000

		return rtblist

	def _get_by_name(self, name: str) -> list:
		for person in self.rtb:
			# TODO: change to 'uri' so it's exact? Seems like overkill
			if name.lower() in person.get('personName', '').lower():
				return person
		
		# They aren't in list, so API shit the bed, meymons can't type, or they are dead (if its Elon, J not furious!)
		return {"personName": "rip", "position": -1, "finalWorth":0, "estWorthPrev": 0}

