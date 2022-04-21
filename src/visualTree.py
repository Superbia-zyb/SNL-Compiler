from pyecharts import options as opts
from pyecharts.charts import Tree
from pyecharts.globals import ThemeType

def PreOrder(node):
    if node == None:
        return None
    data = {"name": node.nodeKind[:-1], "children": []}
    if node.kind != "":
        data["name"] += "\n" + node.kind[:-1]
    if len(node.name) > 0:
        data["name"] += "\n" + node.name[0]
    for i in range(len(node.child)):
        x = PreOrder(node.child[i])
        data["children"].append(x)
    return data

def visTree(root):
    data = PreOrder(root)
    bg_color = "#F6F6F6"
    label_color = "#393D49"
    c = (
        Tree(init_opts=opts.InitOpts(
            width="1650px",
            height="900px",
            theme=ThemeType.LIGHT,
            bg_color=bg_color,
            page_title="Syntax Tree"
        ))
            .add(
            "",
            [data],
            collapse_interval=2,  # 折叠枝点
            #         orient="BT", # 自下向上树图
            #         orient="RL", # 自右向左树图
            orient="TB",  # 自上向下树图
            # layout="radial", # 发散树图
            pos_left='0%',
            pos_right='0%',
            symbol='arrow',
            symbol_size=[10, 10],
            label_opts=opts.LabelOpts(color=label_color, font_size=18, font_weight='bold', font_family='monospace'),
            leaves_label_opts=opts.LabelOpts(color=label_color, font_size=18, font_weight='bold',
                                             font_family='monospace'),
            is_roam=True,  # 是否开启交互
        )
            .set_series_opts(linestyle_opts=opts.LineStyleOpts(color="black", curve=0.6))
            .set_global_opts(title_opts=opts.TitleOpts(title="语法树图", pos_top='10pxs', pos_left='center',
                                                       title_textstyle_opts=opts.TextStyleOpts(color='#2874B2')))
            .render("../data/语法树可视化图.html")
    )
