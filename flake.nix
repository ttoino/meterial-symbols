{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { nixpkgs, ... }: 
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          pyright
          ruff
          (python3.withPackages (pypkgs: with pypkgs; ([
            dataclasses-json
            fonttools
          ] ++ fonttools.optional-dependencies.woff)))
        ];
      };
    };
}
