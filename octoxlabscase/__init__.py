from octoxlabscase.containers import HostsContainer
from octoxlabscase import settings

hosts_container = HostsContainer()
hosts_container.config.from_dict(settings.__dict__)
