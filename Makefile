.PHONY: validate validate-spine validate-negative smoke carry

validate: validate-spine
	python3 tools/validate.py

validate-spine:
	python3 tools/validate_spine.py

smoke:
	python3 tools/smoke.py

carry:
	python3 tools/emit_sourceos_carry.py > examples/sourceos-carry.speechlab.json

validate-negative:
	python3 tools/run_negative_fixtures.py
