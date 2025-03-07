# Maintainer: Cristian Novoa <cnovoa.o@gmail.com>

pkgname=melodymover
pkgver=1.0.0
pkgrel=1
pkgdesc="A powerful and user-friendly desktop application for organizing and managing music collections"
arch=('any')
url="https://github.com/Cristian158/melodymover"
license=('MIT')
depends=('python' 'python-gobject' 'gtk3' 'ffmpeg' 'python-mutagen')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz::https://github.com/Cristian158/melodymover/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

prepare() {
    cd "$srcdir"
    mv "MelodyMover-$pkgver" "$pkgname"
}

build() {
    cd "$srcdir/$pkgname"
    python setup.py build
}

package() {
    cd "$srcdir/$pkgname"
    python setup.py install --root="$pkgdir" --optimize=1
    install -Dm644 LICENSE.md "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
    
    # Ensure the melodymover directory exists
    mkdir -p "$pkgdir/usr/lib/python3.12/site-packages/melodymover"
    
    # Copy all Python files from the source directory
    # install -Dm644 $pkgname/*.py -t "$pkgdir/$(python -c 'import site; print(site.getsitepackages()[0])')/melodymover/"
    install -Dm644 melodymover/*.py -t "$pkgdir/$(python -c 'import site; print(site.getsitepackages()[0])')/melodymover/"
    
    # Copy .glade files if they exist
    # cp -r $pkgname/*.glade "$pkgdir/usr/lib/python3.12/site-packages/melodymover/" || true
    if ls melodymover/*.glade >/dev/null 2>&1; then
        install -Dm644 melodymover/*.glade -t "$pkgdir/$(python -c 'import site; print(site.getsitepackages()[0])')/melodymover/"
    fi
    
    # Ensure the main script is executable
    chmod +x "$pkgdir/usr/bin/melodymover"
}