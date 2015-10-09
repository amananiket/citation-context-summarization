#!/usr/bin/perl
#
# script: print_network_stats.pl
# functionality: Prints various network statistics
#
use strict;
use warnings;

use Getopt::Long;
use File::Spec;
use Clair::Cluster;
use Clair::Network qw($verbose);
use Clair::Network::Centrality::Betweenness;
use Clair::Network::Centrality::Closeness;
use Clair::Network::Centrality::Degree;
use Clair::Network::Centrality::LexRank;
use Clair::Network::Sample::RandomEdge;
use Clair::Network::Sample::ForestFire;
use Clair::Network::Reader::Edgelist;
use Clair::Network::Writer::Edgelist;
use Clair::Network::Writer::GraphML;
use Clair::Network::Writer::Pajek;

sub usage;

my $delim = " ==> ";
my $sample_size = 0;
my $sample_type = "randomedge";
my $fname = "";
my $out_file = "";
my $pajek_file = "";
my $graphml_file = "";
my $extract = 0;
my $stem = 1;
my $undirected = 0;
my $wcc = 0;
my $scc = 0;
my $components = 0;
my $paths = 0;
my $triangles = 0;
my $assortativity = 0;
my $local_cc = 0;
my $all = 0;
my $output_delim = "\t";
my $stats = 0;
my $degree_centrality = 0;
my $closeness_centrality = 0;
my $betweenness_centrality = 0;
my $lexrank_centrality = 0;
my $force = 0;
my $graph_class = "";
my $filebased = 0;
my $input = '';
my $release = 2012;
my $help = 0;

my $res = GetOptions("input=s" => \$input,
					 "release:i" => \$release,
                     "delimout=s" => \$output_delim,
                     "output:s" => \$out_file, "pajek:s" => \$pajek_file,
					 "stats" => \$stats,
                     "graphml:s" => \$graphml_file,
                     "sample=i" => \$sample_size,
                     "sampletype=s" => \$sample_type,
                     "extract!" => \$extract,
                     "stem!" => \$stem, "undirected" => \$undirected,
                     "components" => \$components, "paths" => \$paths,
                     "wcc" => \$wcc, "scc" => \$scc,
                     "triangles" => \$triangles, "verbose!" => \$verbose,
                     "assortativity" => \$assortativity,
                     "localcc" => \$local_cc, "stats!" => \$stats,
                     "all" => \$all,
                     "betweenness-centrality" => \$betweenness_centrality,
                     "degree-centrality" => \$degree_centrality,
                     "closeness-centrality" => \$closeness_centrality,
                     "lexrank-centrality" => \$lexrank_centrality,
                     "force" => \$force,
                     "graph-class=s" => \$graph_class,
                     "filebased" => \$filebased,
					 "help" => \$help);


if(($input ne "acit" && $input ne "pcit" && $input ne "acoll") ||$help)
{
		usage();
		exit;
}

if($input eq "pcit")
{
		$fname = "../$release/networks/paper-citation-network.txt";
}
if($input eq "acit")
{
		$fname = "../$release/networks/author-citation-network.txt";
}

elsif ($input eq "acoll")
{
		$fname = "../$release/networks/author-collaboration-network.txt";
}

else
{
		$fname = "../$release/acl.txt";
}




my $directed = not $undirected;
$Clair::Network::verbose = $verbose;

my $vol;
my $dir;
my $prefix;
($vol, $dir, $prefix) = File::Spec->splitpath($fname);
$prefix =~ s/\.graph//;
if ($all) {
  # Enable all options
  if ($directed) {
    $wcc = 1;
    $scc = 1;
  } else {
    $components = 1;
  }
  $triangles = 1;
  $paths = 1;
  $assortativity = 1;
  $local_cc = 1;
  $betweenness_centrality = 1;
  $degree_centrality = 1;
  $closeness_centrality = 1;
  $lexrank_centrality = 1;
}


if (!$res or ($input eq "")) {
  usage();
}

my $fh;
my @hyp = ();

# make unbuffered
select STDOUT; $| = 1;

if ($verbose) {
  print "Reading in " . ($directed ? "directed" : "undirected") .
    " graph file\n";
}

my $reader = Clair::Network::Reader::Edgelist->new();
my $net;
my $graph;
if ($graph_class ne "") {
  eval("use $graph_class;");
  $graph = $graph_class->new(directed => $directed);
  $net = $reader->read_network($fname, graph => $graph,
                               delim => $delim,
                               directed => $directed,
                               filebased => $filebased);
} 
else {
  $net = $reader->read_network($fname,
                               delim => $delim,
                               directed => $directed,
                               filebased => $filebased,
                               edge_property => "lexrank_transition");
  my $g = $net->{graph};
  my @nodes = $g->vertices();
  my $size = scalar @nodes;
  print "$size number of nodes\n";
  my $numedges = $g->edges();
  print "$numedges number of edges\n";

}

# Sample network if requested
if ($sample_size > 0) {
  if ($sample_type eq "randomedge") {
    if ($verbose) {
      print STDERR "Sampling $sample_size edges from network using random edge algorithm\n"; }
    my $sample = Clair::Network::Sample::RandomEdge->new($net);
    $net = $sample->sample($sample_size);
  } elsif ($sample_type eq "forestfire") {
    if ($verbose) {
      print STDERR "Sampling $sample_size nodes from network using Forest Fire algorithm\n"; }
    my $sample = Clair::Network::Sample::ForestFire->new($net);
    $net = $sample->sample($sample_size, 0.7);
  }
}

#if ((($net->num_documents > 2000) or ($net->num_links > 4000000)) and
#    (!$force) and (!$filebased)) {
#  my $error_msg;
#  $error_msg .= "Network is too large";
#  if ($net->num_documents > 2000) {
#    $error_msg .= " (" . $net->num_documents . " > 2000 nodes)";
#  }
#  if ($net->num_pairs > 4000000) {
#    $error_msg .= " (" . $net->num_pairs . " > 4000000 edges)";
#  }
#  $error_msg .= ", please use sampling\n";
#  die $error_msg;
#}

# If graphviz dotfile is specified, dump network to that file
#if ($fname ne "") {
#  output_graphviz($net, $out_file);
#}

# If Pajek file is specified, dump network to that file
if ($pajek_file ne "") {
  my $export = Clair::Network::Writer::Pajek->new();
  $export->set_name("pajek");
  $export->write_network($net, "$pajek_file");
}

# If GraphML file is specified, dump network to that file
if ($graphml_file ne "") {
  my $export = Clair::Network::Writer::GraphML->new();
  $export->set_name($fname);
  $export->write_network($net, "$graphml_file");
}

if ($out_file ne "") {
  my $export = Clair::Network::Writer::Edgelist->new();
  $export->write_network($net, $out_file);
}

my $component_net;
if ($extract) {
  # Find the largest connected component
  if ($verbose) { print "Extracting largest connected component\n"; }
  print "Original network info:\n";
  print "  nodes: ", $net->num_nodes(), "\n";
  print "  edges: ", scalar($net->get_edges()), "\n";
  $component_net = $net->find_largest_component("weakly");
} else {
  $component_net = $net;
}

if ($stats) {
		$component_net->print_network_info(components => $components,
                                       wcc => $wcc, scc => $scc,
                                       paths => $paths,
                                       triangles => $triangles,
                                       assortativity => $assortativity,
                                       localcc => $local_cc,
                                       delim => $output_delim,
                                       verbose => $verbose);
	print "done printing\n";
}


# Get centrality measures
if ($degree_centrality) {
	print "going to compute degree centrality\n";
  my $degree = Clair::Network::Centrality::Degree->new($component_net);
  my $b = $degree->normalized_centrality();
  open(OUTFILE, "> $prefix.degree-centrality");
  foreach my $v (keys %{$b}) {
    print OUTFILE "$v $output_delim" . $b->{$v} . "\n";
  }
  close OUTFILE;
}
if ($closeness_centrality) {
  my $closeness = Clair::Network::Centrality::Closeness->new($component_net);
  my $b = $closeness->normalized_centrality();
  open(OUTFILE, "> $prefix.closeness-centrality");
  foreach my $v (keys %{$b}) {
    print OUTFILE "$v$output_delim" . $b->{$v} . "\n";
  }
  close OUTFILE;
}
if ($betweenness_centrality) {
  my $betweenness =
    Clair::Network::Centrality::Betweenness->new($component_net);
  my $b = $betweenness->normalized_centrality();
  open(OUTFILE, "> $prefix.betweenness-centrality");
  foreach my $v (keys %{$b}) {
    print OUTFILE "$v$output_delim" . $b->{$v} . "\n";
  }
  close OUTFILE;
}

if ($lexrank_centrality) {
  # Set the cosine value to 1 on the diagonal
  foreach my $v ($component_net->get_vertices) {
    $component_net->set_vertex_attribute($v, "lexrank_transition", 1);
  }

  my $lexrank =
    Clair::Network::Centrality::LexRank->new($component_net);
  my $b = $lexrank->normalized_centrality();
  open(OUTFILE, "> $prefix.lexrank-centrality");
  foreach my $v (keys %{$b}) {
    print OUTFILE "$v$output_delim" . $b->{$v} . "\n";
  }
  close OUTFILE;
}

#
# Print out usage message
#
sub usage
{
  print "usage: $0 -i=\"acit\"|\"acoll\"|\"pcit\" [-d delimiter]  [-release=release_year] [-output=output_file] [-pajek=pajek_file]\n       [-stats] [-graphml=graphml_file] [-sample=sample_size] [-sampletype=sample_type] [-extract] [-components] [-undirected]\n       [-paths] [-wcc] [-cc] [-scc] [-triangles] [-assortativity] [-verbose] [-localcc] [-all] [betweenness-centrality]\n       [-degree-centrality] [-closeness-centrality] [-lexrank-centrality] [-force] [graph-class=graph_class] [-filebased] [-help]\n";
  print "\t--input=\"acit\"|\"acoll\"|\"pcit\"\n";
  print "\t\tInput network\n";
  print "\t--release=release_year\n";
  print "\t\tcan be one of 2008, 2009, 2010 or 2011, defaults to 2011\n";
  print "\t--delim delimiter\n";
  print "\t\tVertices in input are delimited by delimiter character, default is \" ==> \"\n";
  print "\t--delimout output_delimiter\n";
  print "\t\tVertices in output are delimited by delimiter (can be printf format string)\n";
  print "\t--sample sample_size\n";
  print "\t\tCalculate statistics for a sample of the network\n";
  print "\t\tThe sample_size parameter is interpreted differently for each\n";
  print "\t\tsampling algorithm\n";
  print "\t--sampletype sampletype\n";
  print "\t\tChange the sampling algorithm, one of: randomnode, randomedge,\n";
  print "\t\tforestfire\n";
  print "\t\trandomnode: Pick sample_size nodes randomly from the original network\n";
  print "\t\trandomedge: Pick sample_size edges randomly from the original network\n";
  print "\t\tforestfire: Pick sample_size nodes randomly from the original network\n";
  print "\t\t            using ForestFire sampling (see the tutorial for more\n";
  print "\t\t            information)\n";
  print "\t\tBy default uses random edge sampling\n";
  print "\t--output out_file\n";
  print "\t\tIf the network is modified (sampled, etc.) you can optionally write it\n";
  print "\t\tout to another file\n";
  print "\t--pajek pajek_file\n";
  print "\t\tWrite output in Pajek compatible format\n";
  print "\t--extract,  -e\n";
  print "\t\tExtract largest connected component before analyzing.\n";
  print "\t--undirected,  -u\n";
  print "\t\tTreat graph as an undirected graph\n";
  print "\t--scc\n";
  print "\t\tPrint strongly connected components\n";
  print "\t--wcc\n";
  print "\t\tPrint weakly connected components\n";
  print "\t--components\n";
  print "\t\tPrint components (for undirected graph)\n";
  print "\t--paths,  -p\n";
  print "\t\tPrint shortest path matrix for all vertices\n";
  print "\t--triangles,  -t\n";
  print "\t\tPrint all triangles in graph\n";
  print "\t--assortativity,  -a\n";
  print "\t\tPrint the network assortativty coefficient\n";
  print "\t--localcc,  -l\n";
  print "\t\tPrint the local clustering coefficient of each vertex\n";
  print "\t--degree-centrality\n";
  print "\t\tPrint the degree centrality of each vertex\n";
  print "\t--closeness-centrality\n";
  print "\t\tPrint the closeness centrality of each vertex\n";
  print "\t--betweenness-centrality\n";
  print "\t\tPrint the betweenness centrality of each vertex\n";
  print "\t--lexrank-centrality\n";
  print "\t\tPrint the LexRank centrality of each vertex\n";
  print "\n";
  print "example: $0 -input=\"author-citation\"\n";
  print "\n";
  print "Example with sampling: $0 -input=\"author-citation\" --sample 100 --sampletype randomnode -all\n\n";

  exit;
}
