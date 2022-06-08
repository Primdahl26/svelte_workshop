<script lang="ts">
	interface Insight {
		departmentName: string
		employeeEmail: string
		employeeName: string
		id: string
		managerEmail: string
		managersName: string
	}

	let insightQuery = `
      query MyQuery {
        getInsight(skip: 0, limit: 5) {
          departmentName
          employeeEmail
          employeeName
          id
          managerEmail
          managersName
        }
      }
`
	const defaultFields = [
		'id',
		'departmentName',
		'employeeEmail',
		'employeeName',
		'managerEmail',
		'managersName'
	]

	const buildQuery = (skip: number = 0, limit: number = 5, fields: string[] = defaultFields) => {
		return `
      query MyQuery {
        getInsight(skip: ${skip}, limit: ${limit}) {
          ${fields.join(' ')}
        }
      }
    `
	}

	// The callback way
	// const fetchInsight: Promise<Insight[]> = fetch('http://localhost:2000/graphql', {
	// 	method: 'POST',
	// 	headers: {
	// 		'Content-Type': 'application/json'
	// 	},
	// 	body: JSON.stringify({
	// 		query: insightQuery
	// 	})
	// })
	// 	.then((res) => res.json())
	// 	.then((result) => {
	// 		console.log('lol')
	// 		return result.data.getInsight
	// 	})

	// The "oldschool" way
	const fetchInsight = async (): Promise<Insight[]> => {
		const res = await fetch('http://localhost:2000/graphql', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				query: insightQuery
			})
		})

		const result = await res.json()
		return result.data.getInsight
	}

	let data = fetchInsight()

	const refresh = () => {
		data = fetchInsight()
	}

	const modifyData = (event: Event) => {
		// console.log(event.target)
		const data = new FormData(event.target)

		const value = Object.fromEntries(data.entries())

		value.fields = data.getAll('fields')
		console.log(data)
		console.log(data.entries())

		let selectedFields: string[] = ['ost']
		for (const x of data.entries()) {
			selectedFields.push(x[0])
		}

		if (selectedFields) {
			insightQuery = buildQuery((fields = selectedFields))
		}
		refresh()
		return
		insightQuery = `
      query MyQuery {
        getInsight(skip: 0, limit: ${target.value}) {
          id
          departmentName
          employeeEmail
          employeeName
          managerEmail
          managersName
        }
      }
    `
		refresh()
	}
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

<button on:click={refresh}>Refresh data</button>
<br />
<input type="number" on:change={modifyData} value="5" />

<form class="content" on:submit|preventDefault={modifyData}>
	<label for="skip">Skip</label>
	<input id="skip" type="number" value="0" />
	<label for="limit">Limit</label>
	<input id="limit" type="number" value="5" />
	<label for="fields">Fields</label>
	{#each defaultFields as field}
		<input name={field} type="checkbox" checked />
		{field}
		<br />
	{/each}
	<button type="submit">Submit</button>
</form>

<br />
{#await data}
	Henter...
{:then insights}
	{#each insights as insight}
		{#each Object.values(insight) as field}
			{field}
			<br />
		{/each}
		<br />
	{/each}
{/await}
