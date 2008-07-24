#!/usr/bin/perl
#
# Helper script to cleanup the scattered mess of text files in the SMC data
# path - to avoid overloading the spec file making it unreadable. It preserves
# the contents of those text files into a single credits file which gets
# installed in a sane location
#
use strict;

# File name
my $LICFILE = "credits.txt";

# Prefix to installed location
my $PREFIX = "/usr/share/smc";

# Starting directory
my $STARTDIR = "data";

# Open credits file
open (LIC, ">$LICFILE");
print LIC "# Generated automatically by dochelper.pl in the smc RPM.\n\n";
print LIC "Additional licenses and credits for Secret Mayro Chronicles.\n";
print LIC "------------------------------------------------------------\n\n";
close (LIC);

&traverse($STARTDIR);

exit 0;

sub traverse
{
    my $cwd = $_[0];
    system("cd $cwd");
    opendir(DIR, $cwd);
    my @entries = readdir(DIR);
    closedir(DIR);

    foreach my $entry (@entries)
    {
        # Don't recurse current or parent
        next if $entry eq '.';
        next if $entry eq '..';

        # If it's a dir, recurse.
	if (-d "$cwd/$entry") {&traverse("$cwd/$entry");} 

        # Filter out none text files.
        next if ($entry !~ m/^.*txt/g);

	# Skip txt files in this dir because they are configs
        if ($cwd ne 'data/levels')
        {
            if ($entry eq 'all.txt')
            {
                system("echo \"$PREFIX/$cwd/\*\" >> $LICFILE ; cat $cwd/all.txt >> $LICFILE ; echo \"\n\" >> $LICFILE; rm -f $cwd/all.txt");
            }
            else
            { 
		my $ext = $entry;
		my $match = 0;
		$ext =~ s/\.txt/\.ogg/g;
		if (-e "$cwd/$ext") { system("echo \"$PREFIX/$cwd/$ext\" >> $LICFILE"); $match = 1;}
		$ext =~ s/\.ogg/\.ttf/g;
		if (-e "$cwd/$ext") { system("echo \"$PREFIX/$cwd/$ext\" >> $LICFILE"); $match = 1;}
		$ext =~ s/\.ttf/\.png/g;
		if (-e "$cwd/$ext") { system("echo \"$PREFIX/$cwd/$ext\" >> $LICFILE"); $match = 1;}
		if ($match == 0) { system("echo \"$PREFIX/$cwd/$entry\" >> $LICFILE"); }
	        system("cat $cwd/$entry >> $LICFILE ; echo \"\n\" >> $LICFILE ; rm -f $cwd/$entry");
            } 
        }
    }
}
