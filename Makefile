.PHONY: validate smoke carry

validate:
	python3 tools/validate.py

smoke:
	python3 tools/smoke.py

carry:
	python3 tools/emit_sourceos_carry.py > examples/sourceos-carry.speechlab.json
