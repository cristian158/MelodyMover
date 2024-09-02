# Maintainer: Cristian Novoa <cnovoa.o@gmail.com>

pkgname=MelodyMover
pkgver=1.0.0
pkgrel=1
pkgdesc="A powerful and user-friendly desktop application for organizing and managing music collections"
arch=('any')
url="https://github.com/Cristian158/MelodyMover"
license=('MIT')
depends=('python' 'python-gobject' 'gtk3' 'ffmpeg' 'python-mutagen')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz::https://github.com/Cristian158/melodymover/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

prepare() {
    cd "$srcdir"
    mv "$pkgname-$pkgver" "$pkgname"
}

package() {
    cd "$srcdir/$pkgname"
    python setup.py install --root="$pkgdir" --optimize=1
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE.md"
}
