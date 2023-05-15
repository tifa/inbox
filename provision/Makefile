include Make.defs

.PHONY: base
base update:
	ansible-playbook \
		-e admin_email=$(ADMIN_EMAIL) \
		-e mailhost=$(MAILHOST) \
		-e run=$@ \
		playbook.yml

.PHONY: domain
domain:
	ansible-playbook \
		-e hostname=$(HOSTNAME) \
		host.yml

.PHONY: provision
provision:
	ansible-playbook \
		-e admin_email=$(ADMIN_EMAIL) \
		-e mailhost=$(MAILHOST) \
		playbook.yml
