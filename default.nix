{
  poetry2nix ? import (fetchTarball {
    url = "https://github.com/nix-community/poetry2nix/archive/refs/tags/2024.2.2230616.tar.gz";
    sha256 = "0qx2iv57vhgraaqj4dm9zd3dha1p6ch4n07pja0hsxsymjbvdanw";
  }) {}
}:

poetry2nix.mkPoetryApplication {
  projectDir = ./.;
}
