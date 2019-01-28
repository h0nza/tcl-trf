%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%global realname trf

Name:		tcl-%{realname}
Version:	2.1.4
Release:	19%{?dist}
Summary:	Tcl extension providing "transformer" commands
License:	MIT and BSD and LGPLv2+ and GPLv2+ and Public Domain and OpenSSL
URL:		http://tcltrf.sourceforge.net
# We can't use the upstream source because it includes the non-free ripemd implementation
# Source0:	http://downloads.sourceforge.net/tcl%{realname}/%{realname}%{version}.tar.bz2
# To make the clean tarball, just run:
# rm -rf doc/ripemd160.man doc/html/ripemd160.html doc/html/ripemd128.html ./doc/tmml/ripemd128.tmml ./doc/tmml/ripemd160.tmml ./doc/ripemd128.man 
# ./doc/digest/ripemd.inc ./generic/ripemd/ generic/rmd1* tea.tests/rmd1* tests/rmd1*
# We also need to remove the non-free win/msvcrt.dll
# rm -rf win/msvcrt.dll
Source0:	%{realname}%{version}-noripemd.tar.bz2
# BSD licensed haval bits, included code is older and has bad license
Source1:	http://labs.calyptix.com/haval-1.1.tar.gz
Patch0:		trf2.1.3-havalfixes.patch
Patch1:		trf2.1.4-noripemd.patch
Provides:	%{realname} = %{version}-%{release}
BuildRequires:  gcc
BuildRequires:	tcl-devel, tk-devel, zlib-devel, bzip2-devel, openssl-devel
Requires:	tcl(abi) = 8.6
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
Requires:	%{name}%{?_isa} = %{version}-%{release}

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

# Nuke non-modifiable doc
rm -rf doc/painless-guide-to-crc.txt

%build
%configure --with-zlib-lib-dir=%{_libdir} --with-ssl-lib-dir=%{_libdir} --with-bz2-lib-dir=%{_libdir}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -d %{buildroot}%{tcl_sitearch}
mv %{buildroot}%{_libdir}/Trf%{version} %{buildroot}%{tcl_sitearch}/Trf%{version}
rm -rf %{buildroot}%{tcl_sitearch}/Trf%{version}/*.a

%files
%doc doc/ ANNOUNCE ChangeLog DESCRIPTION README*
%{tcl_sitearch}/Trf%{version}

%files devel
%{_includedir}/transform.h
%{_includedir}/trfDecls.h

%changelog
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Tom Callaway <spot@fedoraproject.org> - 2.1.4-13
- modernize spec file

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.1.4-9
- Changed requires to require tcl-8.6

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Wed Sep  4 2013 Tom Callaway <spot@fedoraproject.org> - 2.1.4-7
- remove win/msvcrt.dll from tarball
- delete doc/painless-guide-to-crc.txt

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

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
