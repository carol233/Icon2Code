import re
import androguard.core.bytecodes.dvm
import androguard.core.analysis.analysis
from androguard.misc import AnalyzeAPK

a, d, dx = AnalyzeAPK('/Users/yzha0544/PycharmProjects/gator-3.8/APK/dbmarket.apk')
call_graph = dx.get_call_graph(classname='Lcom/dangbeimarket/ui/movietheme/MovieThemeListActivity;', methodname='onClick')
mds = []
externals = []
for item in call_graph.nodes():
    if isinstance(item, androguard.core.bytecodes.dvm.EncodedMethod):
        mds.append(item)
    elif isinstance(item, androguard.core.analysis.analysis.ExternalMethod):
        externals.append(item)

print(mds)
print(externals)




#
# for item in call_graph.nodes(True):
#     print(type(item))
#     print(item)
#
# for item in call_graph.nodes_iter():
#     print(type(item))
#     print(item)
#
# for item in call_graph.nodes_iter(True):
#     print(type(item))
#     print(item)
#
# for n,nbrsdict in call_graph.adjacency_iter():
#     for nbr, keydict in nbrsdict.items():
#         print(n, nbr)

# match = re.search(r'(L[^;]*;)->[^\(]*\([^\)]*\).*', output)
# if match and match.group(1) not in cs:
#           methods.add(match.group())
# Lcom/dangbeimarket/ui/movietheme/MovieThemeListActivity;->onClick(Landroid/view/View;)V [access_flags=public] @ 0x4c624c