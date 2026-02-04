{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          python313
          python313Packages.pyside6
        ];
        shellHook = ''
          if [ ! -d .venv ]; then
            python3 -m venv .venv
          fi

          source .venv/bin/activate

          pip install -r requirements.txt
        '';
      };

    }
  );
}
