#
# Conditional build:
%bcond_with	bridge_hotkey		# enable the engine hotkeys
#
Summary:	The Anthy engine for IBus input platform
Summary(pl.UTF-8):	Silnik Anthy dla platformy wprowadzania znaków IBus
Name:		ibus-anthy
Version:	1.2.7
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: http://code.google.com/p/ibus/downloads/list
Source0:	http://ibus.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	091a13ff950171981768463993ffb683
URL:		http://code.google.com/p/ibus/
BuildRequires:	anthy-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	gettext-devel >= 0.16.1
BuildRequires:  ibus-devel >= 1.4.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
BuildRequires:	swig-python
Requires:	anthy
Requires:	ibus >= 1.4.0
Requires:	kasumi
Requires:	python-ibus >= 1.4.0
Requires:	python-pygtk-gtk >= 2.15.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/ibus

%description
The Anthy engine for IBus platform. It provides Japanese input method
from libanthy.

%description -l pl.UTF-8
Silnik Anthy dla platformy IBus. Udostępnia metodę wprowadzania znaków
japońskich poprzez libanthy.

%prep
%setup -q

# ibus 1.4.x has symbol attr in EngineDesc; hardcode it so python-ibus
# is not BRed here
%{__sed} -i -e 's,\$SYMBOL_TEST,exit(0),' configure.ac

%build
%{__autoconf}
%configure \
	%{?with_bridge_hotkey:--with-hotkeys}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%{py_sitedir}/anthy.py[co]
%attr(755,root,root) %{py_sitedir}/_anthy.so
%attr(755,root,root) %{_libexecdir}/ibus-engine-anthy
%attr(755,root,root) %{_libexecdir}/ibus-setup-anthy
%{_datadir}/ibus-anthy
%{_datadir}/ibus/component/anthy.xml
