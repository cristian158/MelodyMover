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
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$srcdir/$pkgname-$pkgver"
    python setup.py install --root="$pkgdir" --optimize=1
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
