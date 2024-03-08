"""mod manager"""

import importlib.util
import os
import inspect

class Modules:
    """Class for loading the main modules of PwnKitty. The main modules provide the main 
    functionality of the software. For example, reverse shell handlers, bind shell handlers, ssh handlers, etc. """
    def __init__(self, server: object = None):
        self.server = server
        self.loaded: list[object] = self.load_mods("bin/mods/modules")

    def load_mods(self, path: str) -> list:
        """Load all classes from all modules in the "modules" mod directory."""
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

class CommandModules:
    """ These are modules that become available as commands during an active session. """
    def __init__(self, server: object = None):
        self.server = server
        self.loaded: list[object] = self.load_mods("bin/mods/commands")

    def load_mods(self, path: str) -> list:
        """Load all classes from all modules in the "commands" directory."""
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
    Class for handling the loading and calling of event based modules. Unlike command 
    modules, these are functions that are NOT contained in a class and reside at the top level of
    their file.
     
    Ex. (This will be in the main listening logic)
     
        //Run listener.

        // call_event_mods("on_start")

        // Each loaded mod will be iterated over and if it contains a function named "on_start", it will be executed.
            
            //events/timemod.py
                >>
                //def on_start():
                    print(current_time)

            - this mod would print the current time to the screen any time 'call_event_mods("on_start")' is called

        //Resume. Prepare request to send.

        // call_event_mods("on_send")

            // execute all mod functions named "on_send".

        // Continue
    """

    def __init__(self, server: object = None):
        self.server = server
        self.loaded: list[object] = self.load_mods("bin/mods/events")

    def load_mods(self, path: str) -> list:
        """load all modules from files "events" directory"""
        mods = []
        # Get the names of all the modules in our mod folder.
        mod_files = [f for f in os.listdir(path) if f.endswith('.py')]
        #load each pmod and add it to a list.
        for p in mod_files:
            file_path = os.path.join(path, p)
            spec = importlib.util.spec_from_file_location(p[:-3], file_path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                print(f"Error loading module {p}: {e}")
            mods.append(module)

        return mods

######################################################################################
# These are the names of the currently supported events. it only serves as a reference for now.
    _event_names = [
        "any"
        "on_send",
        "on_recieve",
        "on_task_complete",
        "mutate_payload"
    ]
######################################################################################

    def call_event_mods(self, event:str, args = None):
        """When this function is called with the event name string, it will iterate over each loaded mod
         for a function with that same name as the string passed into it, and then call it.
         """
        for mod in self.ev_mods:
            action = getattr(mod, event, None)
            if callable(action):
                action(self.server, args)


def main():
    """Test function that will run all event based functions from all mods"""
    mods = EventModules()

    for m in mods._event_names:
        mods.call_event_mods(e)

if __name__ == "__main__":
    main()