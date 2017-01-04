
#include <memory>
#include "monitormanager.h"

using namespace std;

MonitorManager::MonitorManager()
    : ChildByIndex<HSMonitor>()
    , focus(*this, "focus")
    , by_name(*this)
{
}
