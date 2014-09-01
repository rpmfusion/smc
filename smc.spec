Name:           smc
Version:        1.9
Release:        17%{?dist}
Summary:        2D platform game that uses OpenGL in a style similar to Super Mario
Group:          Amusements/Games
License:        GPLv3
URL:            http://www.secretmaryo.org
Source0:        http://downloads.sourceforge.net/smclone/%{name}-%{version}.tar.bz2
Source1:        smc.sh
Source2:        dochelper.pl
# suggested in http://thread.gmane.org/gmane.linux.redhat.fedora.rpmfusion.devel/7651/focus=7665
Patch0:         http://repo.calcforge.org/temp/smc-1.9-fix-implicit-linking.patch
# patch from upstream forum, not applied as we use the 0.6 compat pkg
Patch1:         smc-fixes-for-cegui-v0-7.diff
# submitted upstream
Patch2:         smc-1.9-boost-filesystem-v3.patch
# incomplete, must be finished to be able to move to cegui-0.8.x
Patch3:         smc-1.9-cegui-0.8.patch
BuildRequires:  libX11-devel
BuildRequires:  gettext-devel
BuildRequires:  boost-devel >= 1.54
BuildRequires:  cegui06-devel
BuildRequires:  libGLU-devel
BuildRequires:  pkgconfig >= 0.9.0
BuildRequires:  SDL-devel >= 1.2.10
BuildRequires:  SDL_image-devel >= 1.2.0
BuildRequires:  SDL_ttf-devel >= 2.0
BuildRequires:  SDL_mixer-devel >= 1.2.0
BuildRequires:  SDL_gfx-devel
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel
BuildRequires:  autoconf automake libtool
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme

%description
Secret Maryo Chronicles is a 2D platform game that makes use of OpenGL and is
built upon SDL. It is similar to the classic game Super Mario.


%prep
%setup -q
#Fix EOL chars
sed -i 's/\r//' docs/style.css docs/*.html docs/*.txt
%patch0 -p1 -b .patch0
%patch2 -p1
sed -i 's/CEGUI-OPENGL/CEGUI-OPENGL-0.6/' configure.ac
autoreconf -i -f


%build
%configure LIBS=-lboost_system
make %{?_smp_mflags}

# Generate the credit list from lots of little text files scattered around the
# installation. Very messy! A helper script is used to avoid over-complicating
# the spec. Additional processing is done on the credits to fix character
# encoding and to strip 'data/' from the paths because the installation
# location is now different and it's far simpler that altering dochelper.pl
cp %{SOURCE2} . && perl dochelper.pl
sed -i 's/\r//' credits.txt
sed -i 's|data/||g' credits.txt
iconv -f iso8859-1 credits.txt -t utf8 > credits.conv
mv credits.conv credits.txt

# Build desktop file
cat >%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=Secret Maryo Chronicles
GenericName=Platform game
Comment=%{summary}
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ActionGame;
EOF


%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -pm0644 data/icon/window_32.png \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}.bin
install -pm0755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}

desktop-file-install \
%if 0%{?fedora} && 0%{?fedora} < 19
                     --vendor dribble \
%endif
                     --dir %{buildroot}%{_datadir}/applications \
                     %{name}.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc credits.txt docs/*.html docs/*.txt docs/style.css
%{_bindir}/%{name}
%{_bindir}/%{name}.bin
%{_datadir}/%{name}
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


%changelog
* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 1.9-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.9-16
- cegui-0.8.x breaks api in a major way, switch to using cegui06

* Fri May 30 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.9-15
- Rebuild for new libboost

* Tue Aug  6 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.9-14
- Rebuild for new libboost

* Sun Apr  7 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.9-13
- Rebuild for new libboost and cegui

* Thu Nov 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.9-12
- Rebuilt for new boost

* Wed Apr 04 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.9-11
- Rebuild for new libboost

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.9-10
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jul 23 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 1.9-8
- rebuild for new libboost

* Thu Feb 10 2011 Hans de Goede <j.w.r.degoede@hhs.nl> - 1.9-7
- rebuild for new libboost

* Mon Jan  3 2011 Hans de Goede <j.w.r.degoede@hhs.nl> 1.9-6
- rebuild for new cegui

* Wed Aug 25 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.9-5
- rebuild for new libboost

* Sun May 23 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.9-4
- add patch and BR libX11-devel as kevin suggested in
  http://thread.gmane.org/gmane.linux.redhat.fedora.rpmfusion.devel/7651/focus=7665
- add BR gettext-devel
- add "LIBS=-lboost_system" to configure to fix another DSO issue; better
  fix needed in the long term

* Sun May 16 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.9-3
- rebuilt

* Sat Jan 23 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 1.9-2
- rebuild for new libboost

* Sun Oct 25 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 1.9-1
- New upstream release 1.9

* Sat Oct 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8-3
- rebuild for new libboost

* Sat Oct 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8-2
- rebuilt

* Sat Apr 11 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 1.8-1
- New upstream release 1.8

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.7-2
- rebuild for new F11 features

* Thu Jan  1 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 1.7-1
- New upstream release 1.7
- Rebuild for new boost

* Wed Dec  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5-4
- Rebuild for new cegui

* Mon Sep 15 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5-3
- Rebuild for rawhide boost DOWNGRADE to 1.34 <GRRR>

* Sun Aug 17 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5-2
- Rebuild against boost 1.36

* Thu Jul 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5-1
- New upstream release 1.5

* Tue Jan 08 2008 Ian Chapman <packages[AT]amiga-hardware.com> 1.4.1-1
- Upgrade to 1.4.1

* Sun Dec 02 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.3-1
- Upgrade to 1.3
- Minor update to .desktop file due to new validation rules

* Sat Oct 20 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.2-1
- Upgrade to 1.2

* Fri Sep 28 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.1-1
- Upgrade to 1.1
- SPEC cleanups as latest version allows us to streamline the install a bit

* Wed Aug 08 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.0-1
- Upgrade to 1.0
- Changed license field to match new guidelines

* Sat Jun 23 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.99.7-1
- Upgrade to 0.99.7

* Sat Jun 02 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.99.6.1-1
- Upgrade to 0.99.6.1
- Dropped all patches as they are no longer needed.
- Changed .desktop category to Action Games
- Changed .desktop icon as it's now supplied with one.

* Tue Oct 24 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.99.2-1
- Upgrade to 0.99.2
- Dropped fonts patch in favour of using sed
- Updated fiximageset patch
- Added patch to fix the globals header

* Mon Oct 23 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.99.1-2
- Rebuild against latest libraries, seems to fix segfault on some machines

* Thu Sep 07 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.99.1-1
- Upgrade to 0.99.1
- Dropped smc-0.99-fixuint.patch, fixed upstream

* Wed Aug 02 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.99-1
- Upgraded to 0.99
- Fixpaths patch reduced, fewer files need to be fixed
- Added patch to fix location of headers
- Added patch to convert uint to CEGUI::uint to avoid conflict
- Split imageset and fonts into separate patches for easier maintenance

* Sun Jul 16 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.98.1-3
- Added libpng-devel buildrequire for building under mock for fc5

* Sat Jul 08 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.98.1-2
- Corrected EOL chars in additional-licenses.txt
- Removed redundant params from %%setup
- Added automake buildrequire
- Removed pkgconfig buildrequire (required by cegui-devel)
- Moved icon installation to make it freedesktop compliant
- Added %%post and %%postun sections to update icon cache at installation
- Minor cleanups to smc.sh wrapper script
- Moved smc binary installation from /usr/games to /usr/bin/smc.bin
- Enhanced the description

* Sat Jun 24 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.98.1-1
- Initial Release
