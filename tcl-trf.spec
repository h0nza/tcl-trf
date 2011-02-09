%{!?tcl_version: %define tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %define tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%define realname trf

Name:		tcl-%{realname}
Version:	2.1.4
Release:	2%{?dist}
Summary:	Tcl extension providing "transformer" commands
Group:		System Environment/Libraries
License:	MIT and BSD and LGPLv2+ and GPLv2+ and Public Domain and OpenSSL
URL:		http://tcltrf.sourceforge.net
# We can't use the upstream source because it includes the non-free ripemd implementation
# Source0:	http://downloads.sourceforge.net/tcl%{realname}/%{realname}%{version}.tar.bz2
# To make the clean tarball, just run:
# rm -rf doc/ripemd160.man doc/html/ripemd160.html doc/html/ripemd128.html ./doc/tmml/ripemd128.tmml ./doc/tmml/ripemd160.tmml ./doc/ripemd128.man 
# ./doc/digest/ripemd.inc ./generic/ripemd/ generic/rmd1* tea.tests/rmd1* tests/rmd1*
Source0:	%{realname}%{version}-noripemd.tar.bz2
# BSD licensed haval bits, included code is older and has bad license
Source1:	http://labs.calyptix.com/haval-1.1.tar.gz
Patch0:		trf2.1.3-havalfixes.patch
Patch1:		trf2.1.4-noripemd.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides:	%{realname} = %{version}-%{release}
BuildRequires:	tcl-devel, tk-devel, zlib-devel, bzip2-devel, openssl-devel
Requires:	tcl(abi) = 8.5
Requires:	bzip2, zlib, openssl

%description
Trf is an extension library to the script language tcl. It provides 
transformer procedures which change the flow of bytes through a channel 
in arbitrary ways. The underlying functionality in the core is that of 
stacked channels which allows code outside of the core to intercept all 
actions (read/write) on a channel.

Among the applications of the above provided here are compression, 
charset recording, error correction, and hash generation. 

%package devel
Summary:	Development files for tcl-%{realname}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for tcl-%{realname}.

%prep
%setup -q -n %{realname}%{version}
rm -rf generic/haval/ generic/haval.1996
pushd generic
tar xfz %{SOURCE1}
mv haval-1.1 haval/
ln -s haval haval.1996
popd
%patch0 -p1 -b .haval
%patch1 -p1 -b .ripemd

# Get rid of incorrect ripemd docs
rm -rf doc/digest/ripemd.inc doc/man/ripemd128.n doc/man/ripemd160.n doc/ripemd128.man doc/tmml/ripemd128.tmml doc/tmml/ripemd160.tmml

%build
%configure --with-zlib-lib-dir=%{_libdir} --with-ssl-lib-dir=%{_libdir} --with-bz2-lib-dir=%{_libdir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
install -d %{buildroot}%{tcl_sitearch}
mv %{buildroot}%{_libdir}/Trf%{version} %{buildroot}%{tcl_sitearch}/Trf%{version}
rm -rf %{buildroot}%{tcl_sitearch}/Trf%{version}/*.a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/ ANNOUNCE ChangeLog DESCRIPTION README*
%{tcl_sitearch}/Trf%{version}

%files devel
%defattr(-,root,root,-)
%{_includedir}/transform.h
%{_includedir}/trfDecls.h

%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 29 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.1.4-1
- Update to 2.1.4

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.3-3
- fix noripemd patch to resolve undefined symbols (bz 506072)

* Thu Mar 12 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.3-2
- update haval implementation for proper licensing
- drop non-free ripemd bits
- fix license tag

* Tue Feb 3 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.3-1
- initial package for Fedora
