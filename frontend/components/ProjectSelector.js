import React, {useState, useEffect} from 'react'

const ProjectSelector = ({onWorkspaceSelectionChanged, onProjectSelectionChanged}) => {

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [workspaces, setWorkSpaces] = useState([]);
  const [projects, setProjects] = useState([]);

  const [selectedWorkspace, setSelectedWorkspace] = useState("");
  const [selectedProject, setSelectedProject] = useState("");


  const handleWorkspaceChange = async (workspaceId) => {
    setSelectedWorkspace(workspaceId);

    // Notify outside components
    onWorkspaceSelectionChanged(workspaceId);

    setSelectedProject("");  // Reset selected project if workspace selection changed
    await fetchProjects(workspaceId);
  }

  const handleProjectChange = (projectId) => {
    setSelectedProject(projectId);
    onProjectSelectionChanged(projectId);
  }

  const fetchProjects = async (workspaceId) => {
    if (!workspaceId)
    {
      setProjects([]);
      return;
    }

    try {
      const url = `http://localhost:8000/list-projects?workspace_id=${workspaceId}`
      const response = await fetch(url, {
        method: 'GET',
      });

      const data = await response.json();
      setProjects(data);
    } catch (err) {
      console.error("Failed to list project names:", err);
    }
  }


  useEffect(() => {
    const fetchWorkspaces = async () => {
      try {
        setLoading(true);
        
        const url = 'http://localhost:8000/list-workspaces'
        const response = await fetch(url, {
          method: 'GET',
        });

        const data = await response.json();
        setWorkSpaces(data); 
      } catch (err) {
        console.error("Failed to list workspace names:", err);
        setError("Failed to list workspace names.");
      } finally {
        setLoading(false);
      }
    };

    fetchWorkspaces();
  }, []);

  if (loading) {
    return
    <select disabled>
      <option>Loading...</option>
    </select>
  }

  if (error) {
    return 
    <p className='text-red-500'>{error}</p>
  }

  return (
    <div className='flex flex-col gap-4'>
      <label htmlFor="workspace-select">Select Workspace:</label>
      <select className="bg-white dark:bg-slate-900 rounded-lg border border-gray-300" name="workspace-name" id="workspace-select" value={selectedWorkspace} onChange={(e) => handleWorkspaceChange(e.target.value)}>
        <option value="">--</option>
        {workspaces.map((opt) => (
          <option key={opt.id} value={opt.id}>{opt.name}</option>
        ))}
      </select>

      <label>Select Project:</label>
      <select className="bg-white dark:bg-slate-900 rounded-lg border border-gray-300" name="project-name" id="project-select" value={selectedProject} onChange={(e) => handleProjectChange(e.target.value)}>
        <option value="">--</option>
        {projects.map((opt) => (
          <option key={opt.id} value={opt.id}>{opt.name}</option>
        ))}
      </select>
    </div>
  )
}

export default ProjectSelector