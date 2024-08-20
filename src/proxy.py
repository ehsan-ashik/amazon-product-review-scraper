from abc import ABC, abstractmethod

# Proxy generator for smartproxy, oxylabs. CAUTION: Should defer if other proxies are used. Please modify/expand accordingly accordingly
class Proxy(ABC):
	def __init__(self, username, password) -> None:
		self._username = username
		self._password = password
	
	@abstractmethod
	def get_proxy(self):
		pass
		
	
class SmartProxy(Proxy):
	def __init__(self, username, password) -> None:
		super().__init__(username, password)

	
	def get_proxy(self):
		# return f"https://{self.__username}:{self.__password}@us.smartproxy.com:10000"
		proxies = {
			'http': f'http://{self._username}:{self._password}@us.smartproxy.com:10000',
			'https': f'https://{self._username}:{self._password}@us.smartproxy.com:10000',
		}

		return proxies
	


class OxyWUProxy(Proxy):
	def __init__(self, username, password) -> None:
		super().__init__(username, password)

	def get_proxy(self):
		proxies = {
			'http': f'http://{self._username}:{self._password}@unblock.oxylabs.io:60000',
			'https': f'https://{self._username}:{self._password}@unblock.oxylabs.io:60000',
		}

		return proxies