#
# Conditional build:
%bcond_without	bridge_hotkey	# engine hotkeys
%bcond_without	swig		# swig based python-anthy library
#
Summary:	The Anthy engine for IBus input platform
Summary(pl.UTF-8):	Silnik Anthy dla platformy wprowadzania znaków IBus
Name:		ibus-anthy
Version:	1.5.17
Release:	2
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/ibus/ibus-anthy/releases
Source0:	https://github.com/ibus/ibus-anthy/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	10788971d7776189bc96d48d4598d08a
Patch0:		%{name}-proto.patch
URL:		https://github.com/fujiwarat/ibus-anthy/wiki
BuildRequires:	anthy-unicode-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.10
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gobject-introspection-devel >= 0.6.8
BuildRequires:	ibus-devel >= 1.5.28
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-ibus >= 1.5.28
BuildRequires:	python3-pygobject3
BuildRequires:	rpmbuild(macros) >= 1.219
%{?with_swig:BuildRequires:	swig-python}
Requires(post,postun):	glib2-devel >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	anthy-unicode
Requires:	hicolor-icon-theme
Requires:	ibus >= 1.5.28
Requires:	kasumi
Requires:	python3-ibus >= 1.5
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
Requires:	anthy-unicode-devel
Requires:	glib2-devel >= 1:2.26.0

%description devel
Header files for Anthy GObject library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Anthy GObject.

%package -n python3-anthy
Summary:	SWIG based Python interface to Anthy library
Summary(pl.UTF-8):	Oparty na SWIG-u pythonowy interfejs do biblioteki Anthy
Group:		Libraries/Python
Requires:	python3-libs >= 1:3.6
Obsoletes:	python-anthy < 1.5.15

%description -n python3-anthy
SWIG based Python 3 interface to Anthy library.

%description -n python3-anthy -l pl.UTF-8
Oparty na SWIG-u pythonowy interfejs do biblioteki Anthy.

%prep
%setup -q
%patch -P0 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-python=%{__python3} \
	%{?with_swig:--enable-pygtk2-anthy} \
	--with-layout='default' \
	%{?with_bridge_hotkey:--with-hotkeys}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
%if %{with swig}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/_anthy.la
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{pt_PT,pt}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libexecdir}/ibus-engine-anthy
%attr(755,root,root) %{_libexecdir}/ibus-setup-anthy
%{_datadir}/glib-2.0/schemas/org.freedesktop.ibus.engine.anthy.gschema.xml
%{_datadir}/ibus-anthy
%{_datadir}/ibus/component/anthy.xml
%{_datadir}/metainfo/org.freedesktop.ibus.engine.anthy.metainfo.xml
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

%if %{with swig}
%files -n python3-anthy
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_anthy.so
%{py3_sitedir}/__pycache__
%{py3_sitedir}/anthy.py
%endif
