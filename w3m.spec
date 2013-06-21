# TODO add option to remove dependencies

%define gcversion gc6.3
%define Summary   Pager that can also be used as textbased webbrowser

Summary:        %{Summary}
Name:           w3m
Version:        0.5.3
Release:        1
Group:          Networking/WWW
License:        MIT
URL:            http://w3m.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/w3m/%{name}-%{version}.tar.gz
Source2:        w3mconfig
Patch0:         w3m-0.4.1-helpcharset.patch
Patch2:         w3m-0.5.1-gcc4.patch
# String literal fix - AdamW 2008/12
Patch4:		w3m-0.5.2-literal.patch
patch6:		w3m-0.5.3.voidmain.patch
patch7:		w3m-0.5.3.filehandle.patch
patch8:		w3m-0.5.3.opts.patch
Provides:       webclient
BuildRequires:  gpm-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:  imlib-devel >= 1.9.8
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig
#BuildRequires:  termcap-devel
BuildRequires:  ungif-devel
buildrequires:	pkgconfig(gdk-pixbuf-xlib-2.0)
buildrequires:	gc-devel

%description
W3m is a text-based web browser as well as a pager like `more' or
`less'. With w3m you can browse web pages through a terminal emulator
window (xterm, rxvt or something like that). Moreover, w3m can be used
as a text formatting tool which typesets HTML into plain text. w3m also
provides w3mman which is a great manpage browser.

%prep
%setup -q
%patch0 -p1
%patch2 -p1
%patch4 -p1 -b .literal
%patch6 -p1 -b .voidmain
%patch7 -p1 -b .filehandle
%patch8 -p1 -b .opts

#rm -rf gc

cp -a %{SOURCE2} w3mconfig

%build
rm -rf doc{,-jp}/CVS
sed -i s/showaudio/mplayer/ config.h.in

%{configure2_5x} \
                --with-browser=%{_bindir}/www-browser \
                --with-editor=%{_bindir}/vi \
                --with-mailer=/bin/mail \
                --with-termlib=ncurses \
                --enable-alarm \
                --enable-ansi-color \
                --enable-bgcolor \
                --enable-color \
                --enable-cookie \
                --enable-dict \
                --enable-digest-auth \
                --enable-external-uri-loader \
                --enable-gopher \
                --enable-help-cgi \
                --enable-history \
                --enable-image \
                --enable-ipv6 \
                --disable-japanese \
                --enable-keymap=w3m \
                --enable-menu \
                --enable-mouse \
                --enable-nntp \
                --enable-sslverify \
                --enable-w3mmailer \
                --disable-xface \
                --enable-m17n \
                --enable-unicode \
                --with-charset=UTF-8 \
                --with-gc=`pwd`/gc \
								LIBS="-lX11"

echo '#define HAVE_SYS_ERRLIST' >> config.h

make

%install
install -d %{buildroot}/{%{_bindir},{%{_datadir},%{_libdir}}/%{name},%{_mandir}/{,ja_JP.ujis}/man1}

%{makeinstall_std}

install -m0644 doc-jp/w3m.1 %{buildroot}/%{_mandir}/ja_JP.ujis/man1
install -m0644 doc/w3m.1 %{buildroot}/%{_mandir}/man1

install -d %{buildroot}%{_sysconfdir}/w3m
install -m0644 w3mconfig %{buildroot}%{_sysconfdir}/w3m/config

rm -rf %{buildroot}/%{_mandir}/ja*

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README doc doc-jp w3mhelp-lynx_*
%dir %{_sysconfdir}/w3m
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/w3m/config
%attr(0755,root,root) %{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*


%changelog
* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.2-10mdv2011.0
+ Revision: 615429
- the mass rebuild of 2010.1 packages

* Mon Jun 21 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.2-9mdv2010.1
+ Revision: 548422
- try to fix build
- P5: security fix for CVE-2010-2074 (gentoo)

* Thu Apr 08 2010 Rémy Clouard <shikamaru@mandriva.org> 0.5.2-8mdv2010.1
+ Revision: 533194
- Rebuild for new openssl

* Sun Sep 20 2009 Thierry Vignaud <tv@mandriva.org> 0.5.2-6mdv2010.0
+ Revision: 445724
- rebuild

* Tue Dec 23 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.2-5mdv2009.1
+ Revision: 317810
- br gtk+2-devel (needed if using newer gdk-pixbuf)
- make sure it builds with gdk-pixbuf2 not 1 (#45444)
- fix a string literal error (literal.patch)
- hack up a broken test for system syserror in configure (syserror.patch)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 0.5.2-4mdv2009.0
+ Revision: 255777
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0.5.2-2mdv2008.1
+ Revision: 136571
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Sep 04 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.2-2mdv2008.0
+ Revision: 79001
- drop the menu entries (this is a console app, by policy these do not have menu entries: fixes #32702)
- use new draft license policy (-like not -style)

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Tue Jun 05 2007 David Walluck <walluck@mandriva.org> 0.5.2-1mdv2008.0
+ Revision: 35346
- 0.5.2
- bunzip2 patches
- rediff patch static-libgc
- remove patch cvs-20050328 (no longer needed)
- remove patch gc6.2-fix-prelink (wrong gc version)
- change default browser to www-browser
- Import w3m



* Fri Aug 25 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.5.1-7mdv2007.0
- fix summary macro use in menu
- add xdg menu
- cosmetics

* Thu Nov 17 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.5.1-6mdk
- rebuild against openssl-0.9.8

* Tue Apr 19 2005 Oden Eriksson <oeriksson@mandriva.com> 0.5.1-5mdk
- sync with fedora (makes it compile on x86_64)

* Fri Sep 24 2004 Jerome Soyer <saispo@mandrake.org> 0.5.1-4mdk
- Fix menu icons

* Fri Sep 10 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.5.1-3mdk
- Update menu

* Sat Aug 21 2004 Jerome Soyer <saispo@mandrake.org> 0.5.1-2mdk
- fix menu entry

* Sat May  1 2004 Michael Scherer <misc@mandrake.org> 0.5.1-1mdk
- New release 0.5.1

* Fri Apr 23 2004 G?tz Waschk <waschk@linux-mandrake.com> 0.5-3mdk
- buildrequires fix

* Tue Apr 20 2004 Michael Scherer <misc@mandrake.org> 0.5-2mdk 
- enable ncurses to fix segfault in linux console ( thanks rgs for reminding me of the problem )

* Mon Apr 19 2004 Michael Scherer <misc@mandrake.org> 0.5-1mdk
- 0.5
- rpmbuildupdate aware
- fix spec to compile
 
* Thu Sep 25 2003 Han Boetes <han@linux-mandrake.com> 0.4.2-3mdk
- Fix menu's and rightclick menu and imageviewer

* Thu Sep 25 2003 Han Boetes <han@linux-mandrake.com> 0.4.2-2mdk
- Cleanup
- used zsh to find all legal config options. Now we have to find out
  which are usefull.

* Tue Sep 23 2003 Pascal Terjan <CMoi@tuxfamily.org> 0.4.2-1mdk
- New version
- Use configure to select options
- Fix Requires/BuildRequires

* Fri Jul 11 2003 Han Boetes <han@linux-mandrake.com> 0.4.1-3mdk
- fix path to cgi-scripts
- correct macro

* Sun Jun 15 2003 Pascal Terjan <CMoi@tuxfamily.org> 0.4.1-2mdk
- Enforce ipv6 support
- _requires_exceptions on internal perl scripts

* Sun Apr  6 2003 Han Boetes <han@linux-mandrake.com> 0.4.1-1mdk
- Bump
- No longer needed to remove CVS files
- Now really with image support
- spec cleanups/make rpmlint happy

* Sat Jan 11 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.3.2.2-1mdk
- 0.3.2.2

* Thu Dec  5 2002 Han Boetes <han@linux-mandrake.com> 0.3.2-3mdk
- added mouse and ssl support
- added features from the openbsd-port
- removed lang (it wasn't there)

* Fri Nov 29 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.3.2-2mdk
- fix [Bug 572] [w3m] : use correct path for perl interpreter
- fix [Bug 573] [w3m] : add missing manpages

* Tue Nov 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.3.2-1mdk
- "sanitazed spec" release
- new release
- fix %%define abuse
- dont reinvent defined values automatically handled by rpm
- don't pass useless arguments to %%setup
- overall big spec cleaning
- rediff patch 0
- fix menu-title-not-capitalized

* Wed Jan 09 2002 Alexander Skwar <ASkwar@Linux-Mandrake.com> 0.2.4-1mdk
- 0.2.4

* Sun Dec 23 2001 Alexander Skwar <ASkwar@Linux-Mandrake.com> 0.2.3.2-1mdk
- 0.2.3.2

* Fri Dec 21 2001 Alexander Skwar <ASkwar@Linux-Mandrake.com> 0.2.3-1mdk
- 0.2.3
- Update URL
- Redo patch0 (path)

* Fri Nov 16 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.2.1-0.1mdk
- remove patch2

* Tue Aug 28 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.1.11-0.2mdk
- rebuild

* Tue Jan 02 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.1.11-0.1mdk
- used srpm from  Alexander Skwar <ASkwar@Linux-Mandrake.com> :
        - New pre-release version, fixing some crashes
        - Added menu entry

* Fri Aug 11 2000 Alexander Skwar <ASkwar@DigitalProjects.com> 0.1.10-2mdk
- Added Provides: webclient

* Thu Aug 10 2000 Alexander Skwar <ASkwar@DigitalProjects.com> 0.1.10-1mdk
- New version
- Patched the patch to still apply
- Compile with English as the default
- *NO* lynx keys, *NO* mouse
- Use %%{_prefix}/vim instead of /bin/vi

* Wed May 03 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.1.6-2mdk
- fix group
- fix permission on spec

* Tue Jan 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1.6-1mdk
- 0.1.6.
- clean up specs.

* Tue Dec 14 1999 Pixel <pixel@mandrakesoft.com>
- clean up and mandrake adaptation
