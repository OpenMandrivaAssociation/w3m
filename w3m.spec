# TODO add option to remove dependencie

%define gcversion gc6.3
%define	Summary	Pager that can also be used as textbased webbrowser

Summary:	%{Summary}
Name:		w3m
Version:	0.5.1
Release:	%mkrel 7
Group:		Networking/WWW
License:	MIT style
URL:		http://w3m.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/w3m/%{name}-%{version}.tar.bz2
Source1:	http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/%{gcversion}.tar.bz2
Source2:	w3mconfig.bz2
Patch1:		w3m-0.4.1-helpcharset.patch.bz2
Patch2:		w3m-0.5-static-libgc.patch.bz2
Patch3:		w3m-0.5.1-gcc4.patch.bz2
Patch4:		w3m-cvs-20050328.patch.bz2
Patch5:		gc6.2-fix-prelink.patch.bz2
BuildRequires:	termcap-devel
BuildRequires:	imlib-devel >= 1.9.8
BuildRequires:	ungif-devel
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
#BuildRequires:	libgc-devel
BuildRequires:	ncurses-devel
BuildRequires:	gpm-devel
Provides:	webclient
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%define _requires_exceptions	perl(w3mhelp-.*)

%description
W3m is a text-based web browser as well as a pager like `more' or
`less'. With w3m you can browse web pages through a terminal emulator
window (xterm, rxvt or something like that). Moreover, w3m can be used
as a text formatting tool which typesets HTML into plain text. w3m also
provides w3mman which is a great manpagebrowser.

%prep

%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0

rm -rf gc
tar -jxf %{SOURCE1}
mv %{gcversion} gc
(cd gc;
%patch5 -p1
)

bzcat %{SOURCE2} > w3mconfig

%build
sed -i s/showaudio/mplayer/ config.h.in

(cd gc;
make ABI_FLAG="%{optflags} -fPIC" gc.a
mkdir lib
ln -s ../gc.a lib/libgc.a
)

%configure2_5x	--with-browser=mozilla \
		--with-editor=vi \
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
		--disable-kanjisymbols \
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
		--with-gc=$RPM_BUILD_DIR/%{name}-%{version}/gc 

# kanji-symbols breaks menuboxes
# japanese-disables options and rightclick menu
%make

%install
rm -rf %{buildroot}

install -d %{buildroot}/{%{_bindir},{%{_datadir},%{_libdir}}/%{name},%{_mandir}/{,ja_JP.ujis}/man1}

%makeinstall_std

install -m0644 doc-jp/w3m.1 %{buildroot}/%{_mandir}/ja_JP.ujis/man1
install -m0644 doc/w3m.1 %{buildroot}/%{_mandir}/man1

install -d %{buildroot}%{_sysconfdir}/w3m
install -m0644 w3mconfig %{buildroot}%{_sysconfdir}/w3m/config

rm -rf %{buildroot}/%{_mandir}/ja*

# menu entry
mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} << EOF
?package(%{name}): \
	command="%{name} http://www.mandriva.com" \
	title="W3m" \
	longtitle="%{Summary}" \
	section="Internet/Web Browsers" \
	icon="networking_www_section.png" \
	needs="text" \
	xdg="true"
EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=W3m
Comment=%{Summary}
Exec=%{name} http://www.mandriva.com
Icon=%{name}
Terminal=true
Type=Application
Categories=ConsoleOnly;WebBrowser;X-MandrivaLinux-Internet-WebBrowsers;
Encoding=UTF-8
EOF

%find_lang %{name}

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README doc doc-jp w3mhelp-lynx_*
%dir %{_sysconfdir}/w3m
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/w3m/config
%attr(0755,root,root) %{_bindir}/*
%{_libdir}/%{name}
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/%{name}
%{_mandir}/man1/*
