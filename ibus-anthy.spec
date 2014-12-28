#
# Conditional build:
%bcond_without	bridge_hotkey		# disable the engine hotkeys
#
Summary:	The Anthy engine for IBus input platform
Summary(pl.UTF-8):	Silnik Anthy dla platformy wprowadzania znaków IBus
Name:		ibus-anthy
Version:	1.5.6
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://github.com/ibus/ibus-anthy/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	50c8068d789a24c68619136835dcc36f
URL:		https://github.com/fujiwarat/ibus-anthy/wiki
BuildRequires:	anthy-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.10
BuildRequires:	gettext-tools >= 0.16.1
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gobject-introspection-devel >= 0.6.8
BuildRequires:	ibus-devel >= 1.5
BuildRequires:	intltool >= 0.41.1
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
BuildRequires:	swig-python
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	GConf2
Requires:	%{name}-libs = %{version}-%{release}
Requires:	anthy
Requires:	ibus >= 1.5
Requires:	kasumi
Requires:	python-ibus >= 1.5
Requires:	python-pygtk-gtk >= 2:2.15.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/ibus

%description
The Anthy engine for IBus platform. It provides Japanese input method
from libanthy.

%description -l pl.UTF-8
Silnik Anthy dla platformy IBus. Udostępnia metodę wprowadzania znaków
japońskich poprzez libanthy.

%package libs
Summary:	Shared Anthy GObject library
Summary(pl.UTF-8):	Biblioteka współdzielona Anthy GObject
Group:		Libraries
Requires:	glib2 >= 1:2.26.0
Conflicts:	ibus-anthy < 1.4.99.20121006-5

%description libs
Shared Anthy GObject library.

%description libs -l pl.UTF-8
Biblioteka współdzielona Anthy GObject.

%package devel
Summary:	Header files for Anthy GObject library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Anthy GObject
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	anthy-devel
Requires:	glib2-devel >= 1:2.26.0

%description devel
Header files for Anthy GObject library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Anthy GObject.

%prep
%setup -q

# ibus 1.4.x has symbol attr in EngineDesc;
# ibus 1.4.99/1.5+ has symbol attr in IBus.Property
# hardcode it so python-ibus is not BRed here
%{__sed} -i -e 's,\$SYMBOL_TEST,exit(0),' configure.ac

# gettextize will add it again
%{__sed} -i -e '/AC_CONFIG_FILES/s@ po/Makefile\.in@@' configure.ac

%build
%{__gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-layout='default' \
	%{?with_bridge_hotkey:--with-hotkeys}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libexecdir}/ibus-engine-anthy
%attr(755,root,root) %{_libexecdir}/ibus-setup-anthy
%{_datadir}/ibus-anthy
%{_datadir}/ibus/component/anthy.xml
%{_desktopdir}/ibus-setup-anthy.desktop
%{_iconsdir}/hicolor/scalable/apps/ibus-anthy.svg

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libanthygobject-1.0.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libanthygobject-1.0.so.5
%{_libdir}/girepository-1.0/Anthy-9000.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libanthygobject-1.0.so
%{_includedir}/ibus-anthy-1.0
%{_datadir}/gir-1.0/Anthy-9000.gir
