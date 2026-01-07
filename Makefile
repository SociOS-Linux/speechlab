	.PHONY: diar-bootstrap diar-rebuild diar-verify diar-smoketest diar-shell

	diar-bootstrap:
    	./scripts/bootstrap_brew_diar.sh

	diar-rebuild:
    	./scripts/rebuild_diar_env.sh

	diar-verify:
    	./scripts/verify_diar_env.sh

	diar-smoketest:
    	source .venv-diar/bin/activate && ./scripts/smoketest_audioio.sh

	diar-shell:
    	./scripts/diar_shell.sh
