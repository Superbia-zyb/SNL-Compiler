from pyecharts import options as opts
from pyecharts.charts import Tree
from pyecharts.globals import ThemeType

def PreOrder(node):
    if node==None:
        return None
    data = {"name":node.nodeKind, "children":[]}
    if len(node.name) > 0:
        data["name"] = node.nodeKind + ' ' + node.name[0]
    for i in range(len(node.child)):
        x = PreOrder(node.child[i])
        data["children"].append(x)
    return data

def visTree(root):
    data = PreOrder(root)
    c = (
        Tree(init_opts=opts.InitOpts(
            width="1500px",
            height="700px",
            theme=ThemeType.LIGHT,
            bg_color="skyblue",
            page_title="syntax_tree"
        ))
        .add(
            "",
            [data],
            collapse_interval=2,  # 折叠枝点
            #         orient="BT", # 自下向上树图
            #         orient="RL", # 自右向左树图
            orient="TB",  # 自上向下树图
            # layout="radial", # 发散树图
            pos_left='10%',
            pos_right='10%',
            symbol='arrow',
            symbol_size=[10,10],
            label_opts=opts.LabelOpts(color='#F5FF00', font_size=20, font_weight='bold', font_family='monospace'),
            leaves_label_opts=opts.LabelOpts(color='#F5FF00', font_size=20, font_weight='bold', font_family='monospace')
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="语法树图", pos_top='2px', pos_left='center',
                                                       title_textstyle_opts=opts.TextStyleOpts(color='#2874B2')))
        .render("../data/语法树可视化图.html")
    )

