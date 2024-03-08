"""mod manager"""

import importlib.util
import os
import inspect

class Modules:
    def __init__(self, server: object = None):
        self.server = server
        self.mods: list[object] = self.load_mods("bin/mods/modules")

    def load_mods(self, path: str) -> list:
        """Load all the mod modules from a single directory specified in mods settings and instantiate classes found in each module."""
        mods = []
        mod_files = [f for f in os.listdir(path) if f.endswith('.py')]
        for p in mod_files:
            file_path = os.path.join(path, p)
            spec = importlib.util.spec_from_file_location(p[:-3], file_path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                print(f"Error loading module {p}: {e}")
            for name, obj in inspect.getmembers(module, inspect.isclass):

                if obj.__module__ == module.__name__:
                    instance = obj(self.server)
                    mods.append(instance)
        return mods

class EventModules:
    """
    Class for handling the loading and calling of mods. mods are specifically modules that
     supplement the main components of hte program without changing the flow of operations. 
     
    Ex. (This will be in the main scanning logic)
     
        //Run Scan starting logic.

        // call_event_mods("on_start")

        // Each loaded mod will be iterated over and if it contains a function named "on_scan_start", it will be executed.
            
            Ex. //mods/timemod.py
                    //def on_start():
                        print(current_time)

                - this mod would print the current time to the screen any time call_event_mods("on_scan_start") is called

        //Resume scan. Prepared request to send.

        // call_event_mods("on_send")

        // execute all mod functions named "on_send".

        // Continue until finished
    """


    def __init__(self, server: object = None):
        self.server = server
        self.ev_mods: list[object] = self.load_mods("bin/mods/events")

    def load_mods(self, path: str) -> list:
        """load all the mod modules from a single directory specified in mods settings."""
        mods = []
        # Get the names of all the modules in our mod folder.
        mod_files = [f for f in os.listdir(path) if f.endswith('.py')]
        #load each pmod and add it to a list.
        for p in mod_files:
            file_path = os.path.join(path, p)
            spec = importlib.util.spec_from_file_location(p[:-3], file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            mods.append(module)

        return mods

######################################################################################
# These are the names of the currently supported events. it only serves as a reference.
    _event_names = [
        "any"
        "on_send",
        "on_recieve",
        "on_task_complete",
        "mutate_payload"
    ]
######################################################################################


    def call_event_mods(self, event: str, args = None):
        """When this function is called with the event name string, it will iterate over each loaded mod
         for a function with that same name and call it.
         """
        for mod in self.mods:
            action = getattr(mod, event, None)
            if callable(action):
                action(self.server, args)


def main():
    """Test function that will run all functions from all mods"""
    plugs = mods()
    plugs.load_mods("./mods")

    for e in plugs._event_names:
        plugs.call_event_mods(e)

if __name__ == "__main__":
    main()