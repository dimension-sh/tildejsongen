{
  pkgs ? import <nixpkgs> { system = builtins.currentSystem; },
  poetry2nix ? import (fetchTarball {
    url = "https://github.com/nix-community/poetry2nix/archive/refs/tags/2024.2.2230616.tar.gz";
    sha256 = "0qx2iv57vhgraaqj4dm9zd3dha1p6ch4n07pja0hsxsymjbvdanw";
  }) {}
}:

poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  pyproject = ./pyproject.toml;
  poetrylock = ./poetry.lock;

  pythonImportsCheck = [ "tildejsongen" ];

  meta = with pkgs.lib; {
      description = "A simple Python script to generate a `tilde.json` file for Tilde-style servers";
      homepage = "https://github.com/dimension-sh/tildejsongen";
      maintainers = with maintainers; [ nikdoof ];
      license = licenses.mit;
      platforms = platforms.all;
  };
}