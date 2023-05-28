<template>
    <div class="home">
        <div class="container-width">
            <h1 class="flex-title">Jet's Task Tracker</h1>
            <div class="ui raise segment container">
                <form @submit.prevent="create_task">
                    <div class="ui action input focus field">
                        <textarea name="description" placeholder="Add full task description" cols="50" rows="3" v-model="description"></textarea>
                        <button class="ui icon button green is-link" type="submit"><i class="add icon" ></i></button>
                    </div>    
                </form>
            </div>
            <div class="ui container">
                <table class="ui celled striped blue inverted table">
                    <thead>
                        <tr class="center aligned">
                            <th>Task Description</th>
                            <th>Status</th>
                            <th>Remove</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="center aligned" v-for="task in tasks" :key="task.id">
                            <td>{{ task.description }}</td>
                            <td v-if="task.status == false">
                                <button class="ui icon button" id="update_task" @click="update_status(task.id, true)">
                                    <i class="toggle off icon"></i>
                                </button>
                            </td>
                            <td v-else>
                                <button class="ui icon button" id="update_task" @click="update_status(task.id, false)">
                                    <i class="toggle on icon" ></i>
                                </button>
                            </td>
                            <td>
                                <button class="ui icon button mini red" id="remove_task" @click="delete_task(task.id)">
                                    <i class="trash alternate icon" id="remove_task"></i>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: 'HomeView',
        data() {
            return {
                tasks : [],
                description : ''
            }
        },
        async mounted() {
            await this.get_tasks()
        },
        methods : {
            async get_tasks() {
                try {
                    const resp = await axios.get('http://127.0.0.1:5000/tasks')
                    this.tasks = resp.data.tasks
                } catch (err) {
                    console.error(err)
                }

            },
            create_task() {
                axios({
                    method : 'post',
                    url : 'http://127.0.0.1:5000/task',
                    data : {
                        'description' : this.description
                    }
                }).then(resp => {
                    let newTask = {
                        "id" : resp.data.id,
                        "description" : resp.data.description,
                        "status" : resp.data.status
                    }

                    this.tasks.push(newTask)
                    this.description = ''
                }).catch((err) => console.log(err))
            },
            update_status(task_id, new_status) {
                const task = this.tasks.filter(task => task.id === task_id)[0]

                axios({
                    method : 'patch',
                    url : 'http://127.0.0.1:5000/task/' + task_id,
                    data : {
                        'status' : new_status
                    }
                }).then(() => task.status = new_status)
            },
            delete_task(task_id) {
                axios({
                    method : 'delete',
                    url : 'http://127.0.0.1:5000/task/' + task_id
                }).then()

                this.tasks = this.tasks.filter((task)=> task.id !== task_id)
            }
        }

    }
</script>