def report_component_children(component, component_list):
    try:
        component_children = component.GetChildren()
    except:
        return component_list
    if component_children:
        for item in component_children:
            try:
                if item.IsSuppressed:
                    component_list.append(item)
                elif item.GetChildren():
                    component_list.append(item)
                    report_component_children(item, component_list)
                else:
                    component_list.append(item)
            except Exception as ex:
                print("report_component_children failed with {}".format(ex))
                return
        return component_list
    else:
        return component_list
