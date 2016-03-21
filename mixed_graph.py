from sage.graphs.digraph import DiGraph
from sage.graphs.generic_graph import GenericGraph
from sage.graphs.graph import Graph
from sage.plot.arrow import Arrow, CurveArrow
from sage.plot.bezier_path import BezierPath
from sage.plot.line import Line
from sage.sets.set import Set_generic

ARC_COLOR = 'blue'
EDGE_COLOR = 'red'

class MixedGraph(DiGraph):
    def __init__(self, data = None, arcs = None, edges = None,
                 multiedges = True, loops = True, **kargs):
        init = True
        if data is None:
            if edges is None:
                edges = []
            if arcs is None:
                arcs = []
        else:
            if isinstance(data, MixedGraph):
                if edges is not None or arcs is not None:
                    raise ValueError("Edges or arcs should not be specified with a MixedGraph")
                self._edges = data._edges
                self._arcs = data._arcs
                init = False
            elif isinstance(data, Graph):
                if edges is not None:
                    raise ValueError("Edges should not be specified with a Graph")
                edges = data.edges(labels=False)
                if arcs is None:
                    arcs = []
            elif isinstance(data, DiGraph):
                if arcs is not None:
                    raise ValueError("Arcs should not be specified with a DiGraph")
                arcs = data.edges(labels=False)
                if edges is None:
                    edges = []
            elif arcs is not None and edges is None:
                edges = data
                data = None
            else:
                if edges is not None or arcs is not None:
                    raise ValueError("Edges or arcs should not be specified with other data")
                self._edges = []
                self._arcs = []
                for i, e in enumerate(data):
                    u, v = e
                    if isinstance(e, (set, frozenset, Set_generic)):
                        self._edges.append((u, v, i))
                    else:
                        self._arcs.append((u, v, i))
                init = False
        if init:
            n = len(edges)
            self._edges = [(u, v, i) for i, (u, v) in enumerate(edges)]
            self._arcs = [(u, v, i+n) for i, (u, v) in enumerate(arcs)]
        DiGraph.__init__(self, self._edges + self._arcs,
                         multiedges = multiedges, loops = loops, **kargs)
        if isinstance(data, GenericGraph) and data._pos is not None and \
            kargs.setdefault('pos', None) is None and len(data) == len(self):
                self._pos = data._pos

    def graphplot(self, **options):
        options['edge_colors'] = {EDGE_COLOR: self._edges,
                                  ARC_COLOR: self._arcs}
        gp = DiGraph.graphplot(self, **options)
        for i in range(self.size()):
            a = gp._plot_components['edges'][i][0]
            if a.options()['rgbcolor'] == EDGE_COLOR:
                if isinstance(a, CurveArrow):
                    gp._plot_components['edges'][i][0] = \
                        BezierPath(a.path, {'alpha': 1, 'fill': False,
                                            'linestyle': 'solid',
                                            'rgbcolor': EDGE_COLOR,
                                            'thickness': 1, 'zorder': 1})
                else:
                    gp._plot_components['edges'][i][0] = \
                        Line([a.xhead, a.xtail], [a.yhead, a.ytail],
                             {'alpha': 1, 'legend_color': None,
                              'legend_label': None, 'linestyle': 'solid',
                              'rgbcolor': EDGE_COLOR, 'thickness': 1})
        return gp
