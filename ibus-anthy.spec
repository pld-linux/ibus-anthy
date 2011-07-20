#
# Conditional build:
%bcond_without	bridge_hotkey		# disable the engine symbol & hotkeys
#
Summary:	The Anthy engine for IBus input platform
Name:		ibus-anthy
Version:	1.2.6
Release:	0.1
License:	GPL v2+
Group:		Libraries
Source0:	http://ibus.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	894c7311f4d5c96b1fdb8b3795446ead
Patch1:		%{name}-xx-icon-symbol.patch
URL:		http://code.google.com/p/ibus/
BuildRequires:	anthy-devel
BuildRequires:	gettext-devel
%{?with_bridge_hotkey:BuildRequires:  ibus}
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	swig-python
Requires:	anthy
Requires:	ibus >= 1.3.0
Requires:	kasumi
Requires:	python-pygtk-gtk >= 2.15.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Anthy engine for IBus platform. It provides Japanese input method
from libanthy.

%prep
%setup -q
%if %{with bridge_hotkey}
%patch1 -p1
%endif

%build
%if %{with bridge_hotkey}
%{__autoconf}
%configure \
	--with-hotkeys
%else
%configure
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README
%{py_sitedir}/anthy.py*
%attr(755,root,root) %{py_sitedir}/_anthy.so
%{_libdir}/ibus-*-anthy
%{_datadir}/ibus-anthy
%{_datadir}/ibus/component/*