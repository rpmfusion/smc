Name:           smc
Version:        1.5
Release:        4%{?dist}
Summary:        2D platform game that uses OpenGL in a style similar to Super Mario
Group:          Amusements/Games
License:        GPLv3
URL:            http://www.secretmaryo.org
Source0:        http://downloads.sourceforge.net/smclone/%{name}-%{version}.tar.bz2
Source1:        smc.sh
Source2:        dochelper.pl
Patch0:         smc-1.5-boost-1.36.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  boost-devel >= 1.31
BuildRequires:  cegui-devel >= 0.5
BuildRequires:  libGLU-devel
BuildRequires:  pkgconfig >= 0.9.0
BuildRequires:  SDL-devel >= 1.2.10
BuildRequires:  SDL_image-devel >= 1.2.0
BuildRequires:  SDL_ttf-devel >= 2.0
BuildRequires:  SDL_mixer-devel >= 1.2.0
BuildRequires:  SDL_gfx-devel
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme

%description
Secret Maryo Chronicles is a 2D platform game that makes use of OpenGL and is
built upon SDL. It is similar to the classic game Super Mario.


%prep
%setup -q
#patch0 -p1
# Delete useless files to avoid them being installed
rm -f file data/pixmaps/world/tiles/green_1/todo.txt

#Fix EOL chars
sed -i 's/\r//' docs/style.css docs/*.html docs/*.txt


%build
%configure
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
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -pm0644 data/icon/window_32.png \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}.bin
install -pm0755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}

desktop-file-install --vendor dribble \
                     --dir %{buildroot}%{_datadir}/applications \
                     %{name}.desktop


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/%{name}.bin
%{_datadir}/%{name}
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%doc credits.txt docs/*.html docs/license.txt docs/SMC.txt docs/style.css
%doc docs/todo*


%changelog
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

* Sat Dec 02 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.3-1
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
