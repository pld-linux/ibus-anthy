#
# Conditional build:
%bcond_without	bridge_hotkey		# disable the engine hotkeys
#
Summary:	The Anthy engine for IBus input platform
Summary(pl.UTF-8):	Silnik Anthy dla platformy wprowadzania znaków IBus
Name:		ibus-anthy
Version:	1.4.99.20121006
Release:	2
License:	GPL v2+
Group:		Libraries
#Source0Download: http://code.google.com/p/ibus/downloads/list
Source0:	http://ibus.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	518aa503ce40054e0027f2a79c9df640
URL:		http://code.google.com/p/ibus/
BuildRequires:	anthy-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	gettext-devel >= 0.16.1
BuildRequires:	ibus-devel >= 1.4.99
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
BuildRequires:	swig-python
Requires:	anthy
Requires:	ibus >= 1.4.99
Requires:	kasumi
Requires:	python-ibus >= 1.4.99
Requires:	python-pygtk-gtk >= 2:2.15.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/ibus

%description
The Anthy engine for IBus platform. It provides Japanese input method
from libanthy.

%description -l pl.UTF-8
Silnik Anthy dla platformy IBus. Udostępnia metodę wprowadzania znaków
japońskich poprzez libanthy.

%package devel
Summary:	Development tools for ibus
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	anthy-devel
Requires:	glib2-devel

%description devel
The ibus-anthy-devel package contains .so file and .gir files for
developers.

%prep
%setup -q

# ibus 1.4.x has symbol attr in EngineDesc;
# ibus 1.4.99 (1.5) has symbol attr in IBus.Property
# hardcode it so python-ibus is not BRed here
%{__sed} -i -e 's,\$SYMBOL_TEST,exit(0),' configure.ac

%build
%{__autoconf}
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
/sbin/ldconfig
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libexecdir}/ibus-engine-anthy
%attr(755,root,root) %{_libexecdir}/ibus-setup-anthy
%{_datadir}/ibus-anthy
%{_datadir}/ibus/component/anthy.xml
%{_libdir}/girepository-1.0/Anthy-9000.typelib
%attr(755,root,root) %{_libdir}/libanthygobject-1.0.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libanthygobject-1.0.so.5
%{_desktopdir}/ibus-setup-anthy.desktop
%{_iconsdir}/hicolor/scalable/apps/ibus-anthy.svg

%files devel
%defattr(644,root,root,755)
%{_datadir}/gir-1.0/Anthy*.gir
%{_includedir}/ibus-anthy-1.0
%attr(755,root,root) %{_libdir}/libanthygobject-1.0.so
