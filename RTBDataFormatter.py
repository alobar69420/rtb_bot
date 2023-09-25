from RealTimeBillionaires import InformalRTBInterface

class RTBDataFormatter:

	def __init__(self, rtb_source:type(InformalRTBInterface)):
		self.rtb_source = rtb_source

	def format_richlist(self, num: int) -> str:
		richlist = self.rtb_source.get_richlist(num)

		content = 'Standings: \n'
		for ahole in richlist:
			change = ahole['finalWorth'] - ahole['estWorthPrev']
			content += (
				f"#{ahole['position']} - {ahole['personName']}\n"
				f"${ahole['finalWorth']:.2f} billion\n"
				f"Change since last market close: {change:.2f}\n\n"
			)

		return content

	def format_furious(self) -> str:
		furious_data = self.rtb_source.get_furious()
		elon = furious_data[-1]
		pos1_worth = furious_data[0]['finalWorth']
		pos2_worth = furious_data[1]['finalWorth']

		if elon['position'] == 1:
			content = f"Elon is {(elon['finalWorth'] - pos2_worth):.2f} billion in the lead, J furious!!!\n"
		else:
			# Don't worry if this isn't right, code path will never reach here ;P
			content = f"Elon is {(pos1_worth - elon['finalWorth']):.2f} billion behind, Howard furious!!!\n"

		return content

	def format_swong(self, name: str) -> str:
		swongee = self.rtb_source.get_individual(name)
		swong = swongee['finalWorth'] - swongee['estWorthPrev']
		if swong >= 0:
			content = f"{name} is up {swong:.2f} billions since last market close!"
		else:
			content = f"{name} is stuck {abs(swong):.2f} billions since last market close!"

		return content

	def format_position(self, name: str) -> str:
		person = self.rtb_source.get_individual(name)

		if person['position'] > 0:
			content = f"{name} is worth ${person['finalWorth']:.2f} billion and is ranked {person['position']} on the list."
		else:
			content = f"{name}'s broke ass ain't on the list!"

		return content
