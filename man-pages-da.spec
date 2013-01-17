%define LNG da
%define name man-pages-%LNG
%define version 0.1.1
%define release 16

Summary: Danish man pages from the Linux Documentation Project
Name: %{name}
Version: %{version}
Release: %{release}
License: Distributable
Group: System/Internationalization
Patch: manpages-da-0.1.1-manpath.patch
URL: http://www.sslug.dk/locale/man-sider/
Source: http://www.sslug.dk/locale/man-sider/manpages-da-%version.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LNG
Requires: man => 1.5j-8mdk 
BuildRequires: sed grep man
Autoreq: false
BuildArch: noarch

%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP), translated to Danish.  The man pages are
organized into the following sections:

        Section 1:  User commands (intro only)
        Section 2:  System calls
        Section 3:  Libc calls
        Section 4:  Devices (e.g., hd, sd)
        Section 5:  File formats and protocols (e.g., wtmp, %{_sysconfdir}passwd,
                    nfs)
        Section 6:  Games (intro only)
        Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
        Section 8:  System administration (intro only)

%prep
%setup -q -n manpages-da-%{version}
%patch -p1

%build

%install
rm -fr %{buildroot}
make PREFIX=%{buildroot}/usr install

LANG=%LNG DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}/%_mandir/%LNG

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron << EOF
#!/bin/bash
LANG=%LNG %{_bindir}/mandb %_mandir/%LNG
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron

mkdir -p  %{buildroot}/var/cache/man/%LNG

touch %{buildroot}/var/cache/man/%LNG/whatis

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LNG, if there isn't any man page
   ## directory /%_mandir/%LNG
   if [ ! -d %_mandir/%LNG ] ; then
       /bin/rm -rf /var/catman/%LNG
   fi
fi

%post
%create_ghostfile /var/cache/man/%LNG/whatis root root 644

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%doc læsmig AUTHORS ChangeLog
%dir %_mandir/%LNG
%dir /var/cache/man/%LNG
%ghost %config(noreplace) /var/cache/man/%LNG/whatis
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron
%_mandir/%LNG/*



%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-13mdv2011.0
+ Revision: 666366
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-12mdv2011.0
+ Revision: 609317
- rebuild
- fix build
- fix typos

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-11mdv2011.0
+ Revision: 609200
- fix build
- rebuild
- rebuilt for 2010.1

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.1.1-9mdv2009.1
+ Revision: 351567
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.1.1-8mdv2009.0
+ Revision: 223164
- rebuild

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 0.1.1-7mdv2008.1
+ Revision: 152915
- rebuild
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- fix summary-ended-with-dot

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue May 15 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.1-5mdv2008.0
+ Revision: 26773
- clean spec, rebuild for new era


* Thu Jul 24 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.1.1-4mdk
- rebuild

* Mon Jan 20 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.1-3mdk
- build release

* Wed May 29 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.1-2mdk
- use new man-pages-LG template
    - don't rebuild whatis on install since
      - we've already build in package
      - cron will rebuild it nightly and so add other package french man pages
    - adapt to new man-pages-LG template
    - requires man => 1.5j-8mdk for new man-pages framework
    - use new std makewhatis to build whatis in spec and in cron entry 
    - add cron entry to nightly update whatis db
    - whatis db goes into /var/cache/man (so enable ro /usr)
    - standard {Build,}Requires/buildroot/prereq/arc/provides/obsoletes
    - remove duplicated summary

* Fri Mar 08 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.1.1-1mdk
- initial package

