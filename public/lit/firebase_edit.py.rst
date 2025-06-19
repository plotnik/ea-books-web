FB Prompts Edit
===============

Edit Firebase "prompts" collection.

::

  import streamlit as st
  import firebase_admin
  from firebase_admin import credentials, firestore
  import json
  from datetime import datetime
  import os
  from dotenv import load_dotenv

  # Load environment variables
  load_dotenv()

  # Initialize Firebase
  def initialize_firebase():
      """Initialize Firebase connection"""
      try:
          # Check if Firebase is already initialized
          firebase_admin.get_app()
      except ValueError:
          # Initialize Firebase with service account
          if os.path.exists('firebase-credentials.json'):
              cred = credentials.Certificate('firebase-credentials.json')
              firebase_admin.initialize_app(cred)
          else:
              st.error("Firebase credentials file not found. Please add 'firebase-credentials.json' to the project root.")
              st.stop()

  # Initialize Firebase
  initialize_firebase()
  db = firestore.client()

  def add_prompt(title, prompt_text, tags):
      """Add a new prompt to Firebase"""
      try:
          doc_ref = db.collection('prompts').document()
          doc_ref.set({
              'name': title,
              'note': prompt_text,
              'tags': tags,
              'created_at': datetime.now(),
              'updated_at': datetime.now()
          })
          return True
      except Exception as e:
          st.error(f"Error adding prompt: {e}")
          return False

  def get_all_prompts():
      """Get all prompts from Firebase"""
      try:
          prompts = []
          docs = db.collection('prompts').order_by('updated_at', direction=firestore.Query.DESCENDING).stream()
          for doc in docs:
              prompt_data = doc.to_dict()
              prompt_data['id'] = doc.id
              prompts.append(prompt_data)
          return prompts
      except Exception as e:
          st.error(f"Error fetching prompts: {e}")
          return []

  def update_prompt(prompt_id, title, prompt_text, tags):
      """Update an existing prompt"""
      try:
          doc_ref = db.collection('prompts').document(prompt_id)
          doc_ref.update({
              'name': title,
              'note': prompt_text,
              'tags': tags,
              'updated_at': datetime.now()
          })
          return True
      except Exception as e:
          st.error(f"Error updating prompt: {e}")
          return False

  def delete_prompt(prompt_id):
      """Delete a prompt"""
      try:
          db.collection('prompts').document(prompt_id).delete()
          return True
      except Exception as e:
          st.error(f"Error deleting prompt: {e}")
          return False

  def search_prompts(query, tags_filter=None):
      """Search prompts by title, text, or tags"""
      try:
          prompts = get_all_prompts()
          filtered_prompts = []
        
          for prompt in prompts:
              # Search in title and prompt text
              title_match = query.lower() in prompt['name'].lower() if query else True
              text_match = query.lower() in prompt['note'].lower() if query else True
            
              # Filter by tags
              tags_match = True
              if tags_filter:
                  prompt_tags = [tag.lower() for tag in prompt['tags']]
                  tags_match = any(filter_tag.lower() in prompt_tags for filter_tag in tags_filter)
            
              if (title_match or text_match) and tags_match:
                  filtered_prompts.append(prompt)
        
          return filtered_prompts
      except Exception as e:
          st.error(f"Error searching prompts: {e}")
          return []

  # Streamlit UI
  st.set_page_config(
      page_title="Prompt Notes",
      page_icon="📝",
      layout="wide",
      initial_sidebar_state="expanded"
  )

  # Custom CSS for better styling
  st.markdown("""
  <style>
      .main-header {
          font-size: 3rem;
          font-weight: bold;
          color: #1f77b4;
          text-align: center;
          margin-bottom: 2rem;
      }
      .prompt-card {
          background-color: #f8f9fa;
          padding: 1rem;
          border-radius: 10px;
          border-left: 4px solid #1f77b4;
          margin-bottom: 1rem;
      }
      .tag {
          background-color: #e3f2fd;
          color: #1976d2;
          padding: 0.2rem 0.5rem;
          border-radius: 15px;
          font-size: 0.8rem;
          margin-right: 0.5rem;
          display: inline-block;
      }
  </style>
  """, unsafe_allow_html=True)

  # Header
  st.markdown('<h1 class="main-header">📝 Prompt Notes</h1>', unsafe_allow_html=True)

  # Sidebar for navigation
  st.sidebar.title("Navigation")
  page = st.sidebar.selectbox(
      "Choose a page",
      ["View Prompts", "Add New Prompt", "Search Prompts"]
  )

  if page == "View Prompts":
      st.header("All Prompts")
    
      # Get all prompts
      prompts = get_all_prompts()
    
      if not prompts:
          st.info("No prompts found. Add your first prompt!")
      else:
          for prompt in prompts:
              with st.expander(f"📄 {prompt['title']}", expanded=False):
                  col1, col2 = st.columns([3, 1])
                
                  with col1:
                      st.markdown(f"**Title:** {prompt['title']}")
                      st.markdown(f"**Prompt:**")
                      st.text_area("", prompt['prompt_text'], height=150, key=f"view_{prompt['id']}", disabled=True)
                    
                      st.markdown("**Tags:**")
                      for tag in prompt['tags']:
                          st.markdown(f'<span class="tag">{tag}</span>', unsafe_allow_html=True)
                    
                      st.markdown(f"**Created:** {prompt['created_at'].strftime('%Y-%m-%d %H:%M')}")
                      st.markdown(f"**Updated:** {prompt['updated_at'].strftime('%Y-%m-%d %H:%M')}")
                
                  with col2:
                      if st.button("Edit", key=f"edit_{prompt['id']}"):
                          st.session_state.editing_prompt = prompt
                          st.session_state.current_page = "Edit Prompt"
                          st.rerun()
                    
                      if st.button("Delete", key=f"delete_{prompt['id']}"):
                          if delete_prompt(prompt['id']):
                              st.success("Prompt deleted successfully!")
                              st.rerun()

  elif page == "Add New Prompt":
      st.header("Add New Prompt")
    
      with st.form("add_prompt_form"):
          title = st.text_input("Title", placeholder="Enter prompt title...")
          prompt_text = st.text_area("Prompt Text", placeholder="Enter your prompt here...", height=200)
          tags_input = st.text_input("Tags (comma-separated)", placeholder="e.g., coding, python, ai")
        
          submitted = st.form_submit_button("Add Prompt")
        
          if submitted:
              if title and prompt_text:
                  # Process tags
                  tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()] if tags_input else []
                
                  if add_prompt(title, prompt_text, tags):
                      st.success("Prompt added successfully!")
                      st.rerun()
              else:
                  st.error("Please fill in both title and prompt text.")

  elif page == "Search Prompts":
      st.header("Search Prompts")
    
      # Search form
      with st.form("search_form"):
          col1, col2 = st.columns(2)
        
          with col1:
              search_query = st.text_input("Search query", placeholder="Search in title and prompt text...")
        
          with col2:
              tags_filter = st.text_input("Filter by tags (comma-separated)", placeholder="e.g., coding, python")
        
          search_submitted = st.form_submit_button("Search")
    
      # Display search results
      if search_submitted or search_query or tags_filter:
          tags_filter_list = [tag.strip() for tag in tags_filter.split(',') if tag.strip()] if tags_filter else None
          results = search_prompts(search_query, tags_filter_list)
        
          if not results:
              st.info("No prompts found matching your search criteria.")
          else:
              st.success(f"Found {len(results)} prompt(s)")
            
              for prompt in results:
                  with st.expander(f"📄 {prompt['title']}", expanded=False):
                      st.markdown(f"**Title:** {prompt['title']}")
                      st.markdown(f"**Prompt:**")
                      st.text_area("", prompt['prompt_text'], height=150, key=f"search_{prompt['id']}", disabled=True)
                    
                      st.markdown("**Tags:**")
                      for tag in prompt['tags']:
                          st.markdown(f'<span class="tag">{tag}</span>', unsafe_allow_html=True)
                    
                      st.markdown(f"**Updated:** {prompt['updated_at'].strftime('%Y-%m-%d %H:%M')}")

  # Handle editing state
  if hasattr(st.session_state, 'editing_prompt') and st.session_state.editing_prompt:
      st.header("Edit Prompt")
    
      prompt = st.session_state.editing_prompt
    
      with st.form("edit_prompt_form"):
          title = st.text_input("Title", value=prompt['title'])
          prompt_text = st.text_area("Prompt Text", value=prompt['prompt_text'], height=200)
          tags_input = st.text_input("Tags (comma-separated)", value=", ".join(prompt['tags']))
        
          col1, col2 = st.columns(2)
        
          with col1:
              if st.form_submit_button("Update Prompt"):
                  if title and prompt_text:
                      tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()] if tags_input else []
                    
                      if update_prompt(prompt['id'], title, prompt_text, tags):
                          st.success("Prompt updated successfully!")
                          del st.session_state.editing_prompt
                          st.rerun()
                  else:
                      st.error("Please fill in both title and prompt text.")
        
          with col2:
              if st.form_submit_button("Cancel"):
                  del st.session_state.editing_prompt
                  st.rerun()

  # Footer
  st.markdown("---")
  st.markdown("**Prompt Notes** - Built with Streamlit and Firebase") 